import { Injectable} from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class UserService {
    private loggedIn = false;

    constructor(private http: Http) {
        this.loggedIn = !localStorage.getItem('auth_token');
    }

    login(username, password) {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        return this.http.post('http://localhost:8000/api-token-auth/', JSON.stringify({'username': username, 'password': password}), { headers })
        .map(res => res.json())
        .map((res) => {
            if (res.success) {
                localStorage.setItem('auth_token', res.auth_token);
                this.loggedIn = true;
            }
            return res.success;
        });
    }

    logout() {
        localStorage.removeItem('auth_token');
        this.loggedIn = false;
    }

    isLoggedIn() {
        return this.loggedIn;
    }
}