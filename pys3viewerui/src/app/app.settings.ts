import { environment } from '../environments/environment';

export class AppSettings {
    public static envEndpoints = new Map([['local', 'http://localhost:8081/'],[ 'dev', 'http://localhost/'],[ 'sit', 'http://localhost/'], [ 'uat', 'http://localhost/'],[ 'prod', 'http://localhost/']]);
    public static API_ENDPOINT= AppSettings.envEndpoints.get(environment.env);
  }