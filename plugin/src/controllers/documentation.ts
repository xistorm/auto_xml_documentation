import * as vscode from 'vscode';


export class DocumentationController {
    static createDocumentation = (language: string) => {
        const createLanguageDocumentation = (): void => {
            const editor = vscode.window.activeTextEditor;

            if (editor) {
                const document = editor.document;
                const selection = editor.selection;

                const word = document.getText(selection);
                const reversed = word.split('').reverse().join('');
                editor.edit(editBuilder => {
                    editBuilder.replace(selection, reversed);
                });
            }
        };

        return createLanguageDocumentation;
    };
}
