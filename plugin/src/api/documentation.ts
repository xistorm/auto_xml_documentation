import dotenv from 'dotenv';
import axios from 'axios';


dotenv.config();

export class DocumentationAPI {
    private static HOST = process.env.API_HOST || 'localhost';
    private static PORT = process.env.API_PORT || 8000;

    private static buildUrl = (endpoint: string) => {
        return `http://${this.HOST}:${this.PORT}/api/documentation/${endpoint}`
    };

    static create = async (code_text: string, language: string) => {
        const url = this.buildUrl('create');
        const data = { code_text, language };

        const response = await axios.post(url, data);
        const documented_text = await response.data;

        return documented_text;
    };
}
