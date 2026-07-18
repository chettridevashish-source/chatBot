import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '30s', target: 5 },
        { duration: '30s', target: 10 },
        { duration: '30s', target: 20 },
        { duration: '30s', target: 30 },
        { duration: '30s', target: 50 },
        { duration: '30s', target: 0 },
    ],

    thresholds: {
        http_req_failed: ['rate<0.10'],
        http_req_duration: ['p(95)<120000'],
    },
};

const BASE_URL = 'http://127.0.0.1:8000/chat';

const questions = [
    "How do I apply for Income Certificate?",
    "How do I apply for Employment Card?",
    "What is SSO?",
    "What documents are required for ST Certificate?",
    "How do I reset my password?",
    "What is e-District?",
    "How do I register?",
    "How do I apply for OBC Certificate?",
    "How can I update my profile?",
    "What services are available on SSO?",
    "How do I apply for Birth Certificate?",
    "How do I apply for Death Certificate?",
    "What is the eligibility for Income Certificate?",
    "How do I link Aadhaar?",
    "How do I login to SSO?"
];

export default function () {

    const question =
        questions[Math.floor(Math.random() * questions.length)];

    const payload = JSON.stringify({
        question: question,
    });

    const params = {
        headers: {
            "Content-Type": "application/json",
            "Accept": "text/plain",
        },

        timeout: "180s",
    };

    const res = http.post(BASE_URL, payload, params);

    check(res, {
        "Status 200": (r) => r.status === 200,
        "Body received": (r) => r.body.length > 0,
    });

    if (res.status !== 200) {
        console.log("====================================");
        console.log(`Status : ${res.status}`);
        console.log(`Question : ${question}`);
        console.log(`Body : ${res.body}`);
        console.log("====================================");
    }

    sleep(1);
}