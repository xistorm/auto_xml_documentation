import * as vscode from 'vscode';

import { DocumentationAPI } from '../api';


export class DocumentationController {
    static getDocumentedText = (text: string, language: string) => {
        return vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating code documentation',
            cancellable: false,
        }, () => DocumentationAPI.create(text, language));
    };
    
    static displayError = () => {
        vscode.window.showErrorMessage('Something gone wrong. Try another code block.');
    };
    
    static createDocumentation = (language: string) => {
        const createLanguageDocumentation = async () => {
            try {
                const editor = vscode.window.activeTextEditor;
                if (!editor) {
                    return;
                }

                const document = editor.document;
                const selection = editor.selection;

                const text = document.getText(selection);
                const documentedText = await this.getDocumentedText(text, language);

                editor.edit(editBuilder => {
                    editBuilder.replace(selection, documentedText);
                });
            } catch {
                this.displayError();
            }
        };

        return createLanguageDocumentation;
    };
}
