
## Can I contribute?

Please feel free to contribute yourselves by making a pull request or simply open an [issue][issues-url] when you encounter a bug or if you would like to request a new feature.

For any major changes, make sure to open an [issue][issues-url] first. 

For any minor additions or bugfixes, you may simply create a **pull request**. 

When you then create a pull request, be sure to **link the pull request** to the open issue in order to close the issue automatically after merging.

## I want to contribute myself - how do I get started?
To contribute yourselves, create a fork of this repository and run `git clone https://github_link_to_fork` as described [here][development-version].

Then create a development branch from your fork.

Navigate to the folder where the repository was cloned. 

From your development branch run the command:

```bash
$ pip install -e .[dev]
```

This will additionally install packages for development, such as black, pylint, mypy and isort.

When you have finished working on your changes, you can then create a pull request to this repository.

[issues-url]: https://github.com/richardkoehler/pte-xdf/issues
