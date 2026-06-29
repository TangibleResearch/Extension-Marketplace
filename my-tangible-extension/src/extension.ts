export function activate(context) {
  context.commands.register('tangible.helloWorld', () => {
    context.window.info('Hello from Tangible.');
  });

  context.commands.register('tangible.showWorkspace', () => {
    const workspace = context.workspace?.root ?? 'No workspace open';
    context.window.info(`Active workspace: ${workspace}`);
  });
}

export function deactivate() {}
