import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(protected http: HttpClient) { }

  getUsers() {
    return this.http.get('http://127.0.0.1:4100/findUsers');
  }

  newUser(newUser){
    var newUserstr = 'http://127.0.0.1:4100/insertUser'
    return this.http.post(newUserstr, newUser, {});
  }

}
