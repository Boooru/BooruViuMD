![banner](assets/images/banner.png)

# BooruViu

A user-friendly GUI application meant to stream collections of images from your favorite artists and repositories. Fetch images from Twitter, Pixiv, or even your favorite Booru! Switch seamlessly and easily between your favorite image providers, and configure each of them just the way you want!

## Features

BooruViu implements a suite of features, some of which may not be available on certain image sources.
- All
    - Easily download, go to source, reverse-image-search (coming soon), or open in browser
- Boorus:
    - Full booru syntax support, including tags and sorting.
    - Configure individual booru's to blacklist or require specific tags automatically

- Pixiv
    - View a user's illustrations
    - View Daily Rankings (coming soon)
    - View a post's tags (comming soon)
    - View newest by all (coming soon)
    - View newest by followed (coming soon)

- Twitter
    - View a user's tweets
    - Filter by retweet (coming soon)
    - Filter by hashtag (coming soon)
    
- Reddit
    - View any subreddit's image posts
    - View your front-page
    - View /r/all
    - Sort by hot, top, or new (coming soon)
    - Define time range for sorting: hour, day, week, month, etc (coming soon)

### Limitations

- Currently each user will have to supply their own API keys to use the following features:
    - [Twitter](https://developer.twitter.com/en) 
    - [Reddit](https://www.reddit.com/prefs/apps/)
    - [SauceNao](https://saucenao.com/user.php?page=search-api)

    These keys must be supplied to the /tokens/keystore file. I am working on a way to securely deploy the app using *my* keys, but I have yet to figure it out. The good news is, each of the above API keys are very easy to acquire.
    
- BooruViu relies on an unreleased version of Kivy. Pixiv integration called for some deep changes to the way Kivy handles remote image loading. In order to actually run from source, you'll need to install kivy 2.0.0, then copy the contents of the `patch` folder into it. The two files inside the `patch` folder contains the specific updaates necessary to make Kivy function correctly with Pixiv.

### Setup

## From Source
- Run `git clone https://github.com/Boooru/BooruViu.git`
- From inside the cloned folder, run `pip install -r requirements.txt`
- After pip is done, run `pip install saucenao_api`.
  - Pip thinks that `saucenao_api` is in conflict with the other packages, so installing it separately avoids the error messages.
- Create a folder named `tokens`. Create a file inside this folder named `keystore`
- Open `keystore` with your favorite text editor. 
- Supply the keystore with API keys. **This step is not required unless you want to use Twitter, Reddit, or Saucenao integration**

This is how your `keystore` file should look. You may pick and choose which keys to supply as each feature is independent. Note that if you are using Reddit integration, you must supply *all* of the relevent Reddit fields. The links for getting your own API keys can be found in the Limitations section.

```
[Keys]
Saucenao = some api key
Twitter = some other api key
Reddit_app = reddit app id 
Reddit_secret = some different api key
Reddit_username = your reddit username
Reddit_password =  your reddit password
```

- Copy and replace the contents of `/BooruViu/patch/kivy` into your Kivy installation folder. `loader.py` should be replacing a file in Kivy's root folder, and `image.py` should be replacing a file in `/kivy/uix`. 
    - This is a temporary measure that wont be necessary once Kivy reaches its next release.

## Usage

Want to see what it is like to use BooruViu? Take a look down bellow!

### Search a Booru - NSFW

https://user-images.githubusercontent.com/93414885/140667127-bb02a87e-3ce5-4bb4-9a1b-07d7f185ed97.mp4

### Change Providers

https://user-images.githubusercontent.com/93414885/140666468-9dbc30cc-6669-452e-8819-a9d43d5e7c8e.mp4

### Alter Appearance

https://user-images.githubusercontent.com/93414885/140666484-1f74ddb2-2337-4eef-a2c2-6cec313bae44.mp4

### Configure Proivider

