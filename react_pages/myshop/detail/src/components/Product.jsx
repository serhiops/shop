import React from "react";
import { FULL_PATH } from "../config";

const Product = ({product, images, company_name}) => { 
    return(
        <div>
            <div className="container" align='center'>
                    <div className="row">
                        <div className="col-12">
                            <div id="carouselExampleControls" className="carousel slide" data-bs-ride="carousel">
                                <div className="carousel-inner">
                                    <div className="carousel-item active" >
                                        <img src={FULL_PATH + images[0].image} className="img-fluid" alt="product-img" style={{ "height": "400px" }} />
                                    </div>
                                    {images.map(img =>
                                        <div className="carousel-item" key={img.id}>
                                            <img src={FULL_PATH + img.image} className="img-fluid" alt='product-img' style={{ "height": "400px" }}/>
                                        </div>
                                    )}
                                </div>
                                <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
                                    <span className="carousel-control-prev-icon" aria-hidden="false"></span>
                                    <span className="visually-hidden">Previous</span>
                                </button>
                                <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
                                    <span className="carousel-control-next-icon" aria-hidden="false"></span>
                                    <span className="visually-hidden">Next</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <ul className="list-group">
                    <li className="list-group-item">Название : {product.name}</li>
                    <li className="list-group-item">Описание : {product.description}</li>
                    <li className="list-group-item">Продавец : {company_name}</li>
                    <li className="list-group-item">Стоимость : {product.price} грн.</li>
                    <li className="list-group-item">Просмотрело : {product.views} человек</li>
                </ul>
        </div>
    );
}

export default Product;
