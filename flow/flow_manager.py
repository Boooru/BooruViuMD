import enum
import os
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock

from kivy import Logger

from flow.flow_module import FlowPhase, FlowModule
from flow.preprocessing import modules as premodules

# Globals
from util import utils

flow_activate_lock = Lock()
flow_activate_queue = []


class FlowManager:
    __DEFAULT_THREAD_NUM = 1

    def __init__(self, thread_num: int = __DEFAULT_THREAD_NUM):
        self.flows = {
            FlowPhase.PREPROCESSING: {
                "download": premodules.DownloadModule(),
                "convert format": premodules.FormatConvertModule(),
                "upscale image": premodules.UpscaleImageModule()
            }
        }

        self.__thread_pool = ThreadPoolExecutor(thread_num)
        utils.make_temp_dir()

    def __activate(self, flow_name: str):
        flow = self.get_flow(flow_name)

        if self.enabled(flow):
            print("Flow already enabled!")
            return True
        failed = False
        for dependency in flow.prerequisites:
            if not self.enabled(self.get_flow(flow_name)):
                Logger.error("Require flow " + dependency + " not enabled!")
                failed = True

        if failed:
            Logger.error("All required flows must be enabled in order to use: " + flow_name)
            return False

        print("Attempting to activate " + flow_name)
        flow.attempt_to_activate()
        return True

    def get_enabled(self) -> list[str]:
        enabled_list = []
        for key in self.flows:
            for subkey in self.flows[key]:
                if self.enabled(self.flows[key][subkey]):
                    enabled_list.append(self.flows[key][subkey].name)

        return enabled_list

    def enabled(self, flow: FlowModule):
        return self.exists(flow) and flow.is_activated()

    def exists(self, flow: FlowModule):
        return flow \
               and flow.phase in self.flows \
               and flow.name in self.flows[flow.phase] \
               and self.flows[flow.phase][flow.name]

    def get_flow(self, flow_name: str):
        for key in self.flows:
            if flow_name in self.flows[key]:
                return self.flows[key][flow_name]

    def all_flow_names(self):
        flows = []
        for key in self.flows:
            for subkey in self.flows[key]:
                flows.append(subkey)
        return flows

    def submit_activation_request(self, flow_name: str):

        if type(flow_name) == str:
            if flow_name in self.get_enabled():
                return
            flow_activate_lock.acquire()
            flow_activate_queue.append(flow_name)
            flow_activate_lock.release()
            self.__thread_pool.submit(self.__activate, flow_name)

        elif type(flow_name) == list:
            for flow in flow_name:
                if flow_name in self.get_enabled():
                    continue
                flow_activate_lock.acquire()
                flow_activate_queue.append(flow)
                flow_activate_lock.release()
                self.__thread_pool.submit(self.__activate, flow)
