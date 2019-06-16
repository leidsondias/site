console.log("BACKGROUND IS LOADED")

const SITE_DIR = 'projetos/leidson/site/';

const COMMANDS = {
  GENERATE_PYTHON_COMMAND: 'generate-python-command',
  WORKON: 'workon site',
  PYTHON: `python scripts/python/main.py`,
  DEPLOY: './deploy.sh'
}

chrome.commands.onCommand.addListener(function(command) {
  switch (command) {
    case COMMANDS.GENERATE_PYTHON_COMMAND:
      chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        const tab = tabs[0];
        const { url } = tab;
        const command = `${COMMANDS.WORKON}; cd ${SITE_DIR}; ${COMMANDS.PYTHON} ${url} --hugo; ${COMMANDS.DEPLOY}`;
        chrome.tabs.sendMessage(tab.id, {data: command});
      });

      break;
    default:
      break;
  }
});
