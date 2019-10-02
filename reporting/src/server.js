import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors'
import morgan from 'morgan'
import jwt from 'express-jwt'
import jwtAuthz from 'express-jwt-authz'
import jwksRsa from 'jwks-rsa'
import cookieParser from 'cookie-parser'

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

const getTokenFromRequest = (req) => {
    console.log(req.cookies)
    if (req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
        return req.headers.authorization.split(' ')[1];
    } else if (req.query && req.query.token) {
        return req.query.token;
    } else if (req.cookies && req.cookies.access_token) {
        return req.cookies.access_token
    } else if (req.cookies && req.cookies['kc-access']) {
        return req.cookies['kc-access']
    }
    return null;
  }

const checkJwt = jwt({
    // credit to auth0.com for detailed instructions for using node JWT libraries
    secret: jwksRsa.expressJwtSecret({
      cache: true,
      rateLimit: true,
      jwksRequestsPerMinute: 1,
      jwksUri: `${process.env.DISCOVERY_URL}/.well-known/jwks.json`
    }),
  
    getToken: getTokenFromRequest,

    // Validate the audience and the issuer.
    audience: process.env.CLIENT_ID,
    issuer: process.env.DISCOVERY_URL,
    algorithms: ['RS256']
  });


const createRenderServer = (appTemplates, { logger = defaultLogger }) => {
    const createPdf = async (template, data, response) => {
        const started = new Date();
        let reactTemplate;
        try {
            reactTemplate = getBaseTemplate(appTemplates, template);
        } catch (e) {
            logger(WARN, `Template ${template} does not exist`);
            response.status(404).end();
            return;
        }

        // Render React Template
        try {
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
    server.use(morgan('combined'))
    server.use(cookieParser())
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

    server.get('/reports/:template', checkJwt, async(req, res, next) => { 
        try {
            if (!req.user ||
                !req.user.realm_access ||
                !req.user.realm_access.roles.includes('wally-view')) {
                    return res.sendStatus(401)
                }

            logger(INFO, "starting pdf render")
            await createPdf(req.params.template, req.query, res); 
        } catch (e) {
            logger(ERROR, "pdf render failed")
            next(e)
        }
    });

    return server;
};

export default createRenderServer;
