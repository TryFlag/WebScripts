const axios = require('axios');
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

const BASE_URL = 'http://your_URL_here:your_PORT_here';
const JWT_TOKEN = 'your_JWT_here';
const REQUEST_AMOUNT = 10;
const REQUEST_PARAMETER = '/redeem?discountCode[$ne]=a';

if (isMainThread) {
    console.log('Starting ' + REQUEST_AMOUNT + ' parallel threads...');
    const workers = Array.from({ length: REQUEST_AMOUNT }, () => {
        return new Worker(__filename, { workerData: { baseUrl: BASE_URL, jwtToken: JWT_TOKEN } });
    });

    workers.forEach(worker => {
        worker.on('message', message => console.log('Worker response:', message));
        worker.on('error', error => console.error('Worker error:', error));
        worker.on('exit', code => {
            if (code !== 0) {
                console.error(`Worker stopped with exit code ${code}`);
            }
        });
    });
} else {
    const axiosInstance = axios.create({
        baseURL: workerData.baseUrl,
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `jwt=${workerData.jwtToken}`,
        },
    });

    async function sendGetRequest() {
        try {
            const response = await axiosInstance.get(REQUEST_PARAMETER);
            parentPort.postMessage(response.data); 
        } catch (error) {
            parentPort.postMessage(error.response ? error.response.data : error.message);
        }
    }

    sendGetRequest();
}
