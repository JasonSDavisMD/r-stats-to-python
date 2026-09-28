# binder/

Configuration for **[mybinder.org](https://mybinder.org)**, the free public
service behind the "launch binder" badge in the main README. It builds this
repository into a temporary JupyterLab that anyone can open in a browser, with
no account and nothing to install.

* `requirements.txt`: core libraries + JupyterLab, pinned from `workbench/uv.lock`
* `runtime.txt`: Python version
* `postBuild`: installs the `statsbench` toolkit

Binder sessions are **temporary and public-facing**. They shut down after about
10 minutes of inactivity and **nothing is saved**. Use Binder to try the
toolkit, and use your own Codespace or computer for real work.
