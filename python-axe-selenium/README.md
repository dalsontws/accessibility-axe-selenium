# Web Accessibility Project using aXe

## How it works

A sample of less than 40 publicly accessible web pages are taken from various governmental e-services. These pages will them be assessed based on accessibility rules. We used axe, an accessibility testing tool kit that can help identify common issues.

The tool in use, axe includes rules following the Web Content Accessibility Guidelines (WCAG). The tool is currently used together with Selenium WebDriver, that automates the crawling of websites. Our findings are a small sample size of web pages for each domain using the axe tool, and not fully representative of the accessibility of the domain.

For visual representation of the errors, we will be using WAVE (Web Accessibility Evaluation Tool), an online web tool to pinpoint various violations on the pages.

We have incorporated Python and Javascript for various uses of the axe tool.

You can refer to the [Python Version here](https://github.com/dalsontws/accessibility-axe-selenium/tree/master/python-axe-selenium), and the [Javascript Version here](https://github.com/dalsontws/accessibility-axe-selenium/tree/master/js-axe-selenium) for more in-depth installation and usage instructions.

## Recommended: User Setup (Ansible)

Steps recommended to quickly get started on automated accessibility testing with the repo.

1. Ensure you are in the [ansible directory](https://github.com/dalsontws/accessibility-axe-selenium/tree/master/python-axe-selenium/ansible)
2. To run the installer playbook from your terminal, run: `ansible-playbook ansible-playbook-virtualenv.yml -i inventory.yml -c local`
3. To run the chrome-driver installation playbook from your terminal, run: ansible-playbook ansible-task-chrome-driver.yml -i inventory.yml -c local --extra-vars "ansible_become_pass=YOURPASSWORDHERE"

## Acknowledgements

[Deque](https://www.deque.com/axe/) for the [axe-core api](https://github.com/dequelabs/axe-core)
