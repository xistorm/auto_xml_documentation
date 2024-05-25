import * as vscode from 'vscode';

import { DocumentationAPI } from '../api';


export class DocumentationController {
    static createDocumentation = (language: string) => {
        const createLanguageDocumentation = async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }

            const document = editor.document;
            const selection = editor.selection;

            const text = document.getText(selection);
            const documented_text = await DocumentationAPI.create(text, language);
            editor.edit(editBuilder => {
                editBuilder.replace(selection, documented_text);
            });
        };

        return createLanguageDocumentation;
    };
}
