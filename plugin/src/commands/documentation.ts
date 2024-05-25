import * as vscode from 'vscode';

import { DocumentationController } from '../controllers';


export abstract class DocumentationCommand {
    protected static command: string = 'xml-documentation-generation';

    public static register = (language: string): vscode.Disposable => {
        const callback = DocumentationController.createDocumentation(language);
        const name = `${this.command}.${language}`;

        return vscode.commands.registerCommand(name, callback);
    };
}
