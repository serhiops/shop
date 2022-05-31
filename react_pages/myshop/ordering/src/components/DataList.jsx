import { useState } from "react";
import { USER_URL } from "../config";
import {setError, setSuccess} from "./Alert";
import getCookie from "../getCookie";
import $  from "jquery";
import CSRFToken from "../csrfToken";

const DataList = ({ salesman, product, current_user }) => {
    let [isChange, setIsChange] = useState(false);
    let [name, setName] = useState(current_user.first_name);
    let [sername, setSername] = useState(current_user.last_name);
    let [phoneNumber, setPhoneNumber] = useState(current_user.number_of_phone)

    const saveUserData = (e) => {
        if (name.length < 2 || sername.length <2 ){
            setError("Имя и фамилия должны иметь не меньше 2 символов");
            return;
        } if (phoneNumber.length !== 10){
            setError("Номер телефона не должен иметь код страны и состоять из 10 цифр!");
            return;
        }
        $.ajax({
            type:'PATCH',
            url: USER_URL + String(current_user.id) + "/",
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            data:{
                first_name: name,
                last_name: sername,
                number_of_phone: phoneNumber,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success:({ user, error })=>{
                if (error) {
                    setError("Вы неверно ввели данные!");
                } else {
                    setName(user.first_name);
                    setSername(user.last_name);
                    setPhoneNumber(user.number_of_phone);
                    setSuccess('Вы успешно изменили данные!');
                    setIsChange(false);
                }
            }
        })
    }

    return (
        <div>
            {!isChange ?
                <div>
                    <ul className="list-group" id="userData">
                        <li className="list-group-item">Компания : {salesman.company}</li>
                        <li className="list-group-item">Продавец : {salesman.first_name}  {salesman.last_name}</li>
                        <li className="list-group-item" id="name">Покупатель :{name}  {sername}</li>
                        <li className="list-group-item" id="phone">Контактный номер : {phoneNumber}</li>
                        <li className="list-group-item">Товар : {product.name}</li>
                        <li className="list-group-item">Цена : {product.price}</li>
                    </ul>
                    <div className="col-3">
                        <button type="submit" className="btn btn-primary btn-block col-12" onClick={() => { setIsChange(true) }} >Изменить личные данные</button>
                    </div>
                </div>
                :
                <div>
                    <form  name="data-form">
                        <CSRFToken/>
                        <li className="list-group-item" id='name_user' >Имя: <input type="text" className="form-control" value={name} onChange={e => { setName(e.target.value) }} /></li>
                        <li className="list-group-item" id='name_user'>Фамилия: <input type="text" className="form-control" value={sername} onChange={e => { setSername(e.target.value) }} /></li>
                        <li className="list-group-item" id='phone_number_user'>Контактный номер : <input type="text" className="form-control" value={phoneNumber} onChange={e => { setPhoneNumber(e.target.value) }} /></li>
                        <div className="col-3">
                            <button type="submit" className="btn btn-success btn-block col-12 " style={{ 'marginTop': '5px' }} onClick={saveUserData}>Изменить личные данные</button>
                        </div>
                    </form>
                </div>}
        </div>

    )
}

export default DataList;