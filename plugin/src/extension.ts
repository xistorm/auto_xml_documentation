import * as vscode from 'vscode';

import { DocumentationCommand } from './commands';


const languages = ['ru', 'en'];

export const activate = (context: vscode.ExtensionContext) => {
	languages.forEach(language => {
		const command = DocumentationCommand.register(language);
		context.subscriptions.push(command);
	});
};

