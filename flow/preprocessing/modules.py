import os
import re

from kivy import Logger

import assets.strings
import main
from flow.flow_module import FlowModule, FlowModuleState, FlowPhase


class DownloadModule(FlowModule):

    def __init__(self):
        super(DownloadModule, self).__init__()
        self.name = "download"
        self.phase = FlowPhase.PREPROCESSING

    def is_activated(self):
        return main.async_downloader is not None

    def __setup(self):
        try:
            import main
            import flow
            if not main.async_downloader:
                main.async_downloader = flow.preprocessing.download.AsyncDownloader()
            self.state = FlowModuleState.AVAILABLE
        except:
            Logger.error("Couldn't set up flow module: " + self.name + "!")
            raise


class FormatConvertModule(FlowModule):
    def __init__(self):
        super(FormatConvertModule, self).__init__()
        self.name = "convert format"
        self.phase = FlowPhase.PREPROCESSING

    def is_activated(self):
        return True

    def __setup(self):
        try:
            import format_convert
            self.state = FlowModuleState.AVAILABLE
        except:
            Logger.error("Couldn't set up flow module: " + self.name + "!")
            raise


class UpscaleImageModule(FlowModule):
    path_to_exe = None

    def __init__(self):
        self.phase = FlowPhase.PREPROCESSING
        super(UpscaleImageModule, self).__init__("upscale image", self._setup, self.check_for_bin)
        self.check_for_bin()

    def interface(self, in_path, out_path, denoise=0, scale=2, ext="png", load_proc_save="1:2:2"):
        if self.path_to_exe and os.path.isfile(self.path_to_exe):
            command = self.path_to_exe + " -i {i} -o {o} -n {n} -s {s} -j {j} -f {f}".format(i=in_path,
                                                                                             o=out_path,
                                                                                             n=denoise,
                                                                                             s=scale,
                                                                                             j=load_proc_save,
                                                                                             f=ext)


    def is_activated(self):
        print("UpscaleImageModule is active:" + str(self.path_to_exe is not None))
        return self.path_to_exe is not None

    def _setup(self):
        print("Running setup for: " + self.name)
        self.make_bin_dir()
        from kivy import platform
        url = None
        if platform == "win":
            url = assets.strings.MODULE_UPSCALE_WINDOWS_URL

        elif platform == "linux":
            url = assets.strings.MODULE_UPSCALE_LINUX_URL

        elif platform == "macosx":
            url = assets.strings.MODULE_UPSCALE_OSX_URL

        else:
            Logger.error("Can't find upscale provider for " + platform + "!")
            raise EnvironmentError("Unsupported platform")

        import requests
        import shutil
        zip_save_path = 'temp/upscaleprovider.zip'
        zip_extract_path = assets.strings.MODULE_UPSCALE_BIN_PATH
        dist = requests.get(url)  # Get the zip file with our upscale provider
        open(zip_save_path, 'wb').write(dist.content)  # Save it to disk

        shutil.unpack_archive(zip_save_path, zip_extract_path, "zip")

        os.remove(zip_save_path)
        self.state = FlowModuleState.AVAILABLE

    def check_for_bin(self):
        rootdir = "./bin/upscaleprovider"
        found_dir = None
        regex_dir = re.compile('waifu2x-ncnn-vulkan-*')
        regex_file = re.compile('waifu2x-ncnn-*')

        # Look for dir containing exe
        for root, dirs, files in os.walk(rootdir):
            for directory in dirs:
                if regex_dir.match(directory):
                    found_dir = directory

        if not found_dir:
            return False

        # Look for executable
        for root, dirs, files in os.walk(rootdir + "/" + found_dir):
            for file in files:
                if regex_file.match(file):
                    Logger.info("executable found!")
                    self.path_to_exe = rootdir + "/" + found_dir + "/" + file
                    print(self.path_to_exe)
                    return True

        return False

    def make_bin_dir(self):
        print("Making bin")
        from pathlib import Path
        path = Path(assets.strings.MODULE_UPSCALE_BIN_PATH)
        os.makedirs(path, exist_ok=True)
        return True



