import { Injectable, OnInit, OnDestroy } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch'
import { Observable } from 'rxjs/Rx';
import { AppSettings } from '../../app/app.settings';
import { LoginModel } from '../models/index';
import { environment } from '../../environments/environment';

@Injectable()
export class Pys3viewerService implements OnInit {
  private apiUrl:String;

  constructor(private http: Http) {}
  ngOnInit(){
        //this.apiUrl=  (environment.env=='local') ?  AppSettings.API_ENDPOINT : AppSettings.API_ENDPOINT+'api/';

  }


  postS3bucketRequest(loginInfo: LoginModel): Observable<any>{
          this.apiUrl = 'http://localhost:8081/';  
    return this.http.post(this.apiUrl+'buckets', loginInfo, this.getOptions()).map((response: Response)=>{response.json().data});
  }

  postS3bucketObjectRequest(loginInfo: LoginModel): Observable<any>{
          this.apiUrl = 'http://localhost:8081/';    
    return this.http.post(this.apiUrl+'bucketobjects', loginInfo, this.getOptions()).map((response: Response)=>{response.json().data});
  }

    private getOptions(): RequestOptions {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions();
    options.headers = headers;
    return options;
  }

}
