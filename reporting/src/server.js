import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors'

const CONTENT_TYPE = 'Content-Type';
const INFO = 'info';
const WARN = 'warning';
const ERROR = 'error';

const defaultLogger = (level, message) => {
    console.log(`${new Date()} ${level}: ${message}`);
};

const getBaseTemplate = (templates, template) => {
    if (template in templates) {
        return templates[template];
    }
    throw new Error(`No template defined with name ${template}`);
};

const createRenderServer = (appTemplates, { logger = defaultLogger }) => {
    const createPdf = async (template, data, response) => {
        const started = new Date();
        try {
            let reactTemplate;
            try {
                reactTemplate = getBaseTemplate(appTemplates, template);
            } catch (e) {
                logger(WARN, `Template ${template} does not exist`);
                response.status(404).end();
                return;
            }

            // Render React Template
            const readStream = await reactTemplate(data)
            response.set(CONTENT_TYPE, 'application/pdf');
            readStream.pipe(response);

            // When the stream end the response is closed as well
            readStream.on('end', () => logger(INFO, `Rendered template ${template} in ${new Date() - started}ms`));
        } catch (e) {
            logger(ERROR, `Error occurred while rendering: "${e}"`);
            response.status(500).end();
        }
    };

    const server = express();

    server.use(bodyParser.json({ limit: '1mb' }));
    server.use(bodyParser.urlencoded({ limit: '1mb', extended: true }));

    const whitelist = ['http://localhost:8080', 'http://127.0.0.1:8080', 'http://maps.gov.bc.ca']
    const corsOptions = {
        origin: function(origin, callback) {
            if (whitelist.indexOf(origin) !== -1) {
                callback(null, true)
            } else {
                callback(new Error('Not allowed by CORS'))
            }
        }
    }
    server.use(cors()) // TODO update cors to only trusted hosts using above options whitelist


    server.get('/favicon.ico', (req, res) => res.status('404').end());
    server.get('/health', (req, res) => res.status('200').end());

    server.get('/reports/:template', (req, res) => createPdf(req.params.template, req.query, res));
    server.post('/reports/:template', (req, res) => {
        const data = req.body;
        Object.keys(req.query).forEach((value) => {
            if (data[value]) {
                logger(WARN, `Body property '${value}' was overwritten by query param.`);
            }
            data[value] = req.query[value];
        });
        createPdf(req.params.template, data, res);
    });

    return server;
};

export default createRenderServer;
