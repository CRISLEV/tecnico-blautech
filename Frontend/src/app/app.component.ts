import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { UserService } from './users.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit{
  title = 'practica1sa';
  displayedColumns: string[] = ['position', 'username', 'name', 'email', 'age', 'employeeid', 'eliminar'];
  dataSource = ELEMENT_DATA;
  Users: any[] = [];
  UserName:any ;
  Name:any ;
  Email:any ;
  Age:any ;
  Password:any ;
  EmpID:any ;

  constructor(
    protected Userservice: UserService,
    private changeDetectorRefs: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.lstUsers();
  }

  refresh() {
    console.log("refreshing...");
    this.dataSource = [...this.dataSource];
    this.changeDetectorRefs.detectChanges();
  }

  lstUsers(){
    this.Userservice.getUsers()
    .subscribe(
      (data) => {
        console.log(data);
        this.Users = data['users'];
        console.log(this.Users);
        ELEMENT_DATA = [];
        for (let i = 0; i < this.Users.length; i++) {
          console.log(this.Users[i].name);
          ELEMENT_DATA.push({position: (i+1), username: this.Users[i].username, name: this.Users[i].name, email: this.Users[i].email,
                             age: this.Users[i].age, password:this.Users[i].password, employeeid: this.Users[i].employeeid});
        }
        this.dataSource = ELEMENT_DATA;
        console.log(this.dataSource);
        this.refresh();
      },
      (error) => {
        console.error(error);
      }
    );
  }

  actionBtn(){
    console.log(this.UserName);
    var newUser = {username: this.UserName, name: this.Name, email: this.Email,
                  age: this.Age, password:this.Password, employeeid: this.EmpID};
    var response = this.Userservice.newUser(newUser)
    .subscribe(
      data => {// Success
        console.log(data);
        alert('Contacto creado!');
        this.lstUsers();
      },
      (error) => {
        console.error(error);
      }
    );
  }

  deleteBtn(row){
    console.log(row);
    var response = this.Userservice.delUser(row.username)
    .subscribe(
      data => {// Success
        console.log(data);
        alert('Contacto eliminado!');
        this.lstUsers();
      },
      (error) => {
        console.error(error);
      }
    );
  }

}
export interface UserElement {
  position: number;
  username:string;
  name: string;
  email:string;
  age: number;
  password:string;
  employeeid:string;
}

var ELEMENT_DATA: UserElement[] = [
];
