Refissue
=========
Automatic GitHub-Issues Suggestion Tools

What is this tool?
-------------------
This app gives you similar past issues on your repository whenever you post a new issue.

![img](https://raw.github.com/addsict/refissue/master/imgs/img1.png)

How to install
----------------

1. Create a new application on [Google App Engine](https://appengine.google.com/).

    This tool needs web-hook endpoint and currently only supported on Google App Engine.

1. Build application

    ```sh
    $ python bootstrap.py
    $ ./bin/buildout
    ```

1. Generate a GitHub personal API token by using cURL command and store it into `credential.json`.

    ```sh
    # Enter your GitHub user name into `USER`.
    $ curl -u USER -d '{"scopes": ["repo"]}' https://api.github.com/authorizations > credential.json
    ```

1. Create a GitHub web hook. Use above created application url as hook endpoint.

    The default hook endpoint is `http://YOUR_APP.appspot.com/hook`

    ```sh
    $ ./bin/create_hook --user=USER --repository=REPOSITORY_NAME --endpoint=HOOK_ENDPOINT
    ```

1. Deploy your Google App Engine application

    ```sh
    $ ./parts/google_appengine/appcfg.py update -a APPLICATION_NAME .
    ```

FAQ
-----
- How can we delete a web hook?
    - You can delete it on th web(GitHub repository settings page)


License
---------
This tools are distributed by MIT license.
