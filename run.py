const fs = require('fs');
const axios = require('axios');

// Fungsi untuk membaca file
const readFileLines = (filePath) => {
    try {
        return fs.readFileSync(filePath, 'utf-8').split('\n').filter(line => line.trim());
    } catch (err) {
        console.error(`Error reading file ${filePath}:`, err);
        return [];
    }
};

// Konfigurasi utama
const proxiesFilePath = './proxies.txt';
const tokensFilePath = './np_tokens.txt';

// Membaca file
const proxies = readFileLines(proxiesFilePath);
const tokens = readFileLines(tokensFilePath);

if (proxies.length === 0 || tokens.length === 0) {
    console.error('Proxies or NP tokens are missing. Ensure both files are populated.');
    process.exit(1);
}

// Fungsi untuk menjalankan Nodepay dengan proxy dan token
const runNodepay = async (proxy, token) => {
    try {
        console.log(`Running Nodepay with proxy: ${proxy} and token: ${token}`);

        // Contoh request menggunakan axios dan proxy
        const response = await axios.post('https://nodepay.api/extension', {
            npToken: token,
        }, {
            proxy: {
                protocol: 'http',
                host: proxy.split('@')[1].split(':')[0],
                port: parseInt(proxy.split(':')[2]),
                auth: {
                    username: proxy.split('//')[1].split(':')[0],
                    password: proxy.split(':')[1].split('@')[0],
                },
            },
        });

        console.log(`Success for token ${token}:`, response.data);
    } catch (err) {
        console.error(`Error for token ${token} with proxy ${proxy}:`, err.message);
    }
};

// Iterasi menjalankan Nodepay
(async () => {
    for (let i = 0; i < Math.min(proxies.length, tokens.length); i++) {
        const proxy = proxies[i];
        const token = tokens[i];
        await runNodepay(proxy, token);
    }
})();
