import React from "react";

const DOMAIN = 'http://127.0.0.1:8000'
const Product = ({product, images, company_name}) => { 
    return(
        <div>
            <div className="container" align='center'>
                    <div className="row">
                        <div className="col-12">
                            <div id="carouselExampleControls" className="carousel slide" data-bs-ride="carousel">
                                <div className="carousel-inner">
                                    <div className="carousel-item active" style={{ "height": "400px" }}>
                                        <img src={DOMAIN + images[0].image} className="d-block w-25" alt="asd" style={{ "height": "400px" }} />
                                    </div>
                                    {images.map(img =>
                                        <div className="carousel-item" style={{ "height": "400px" }} key={img.id}>
                                            <img src={DOMAIN + img.image} className="d-block w-25" alt='asd' style={{ "height": "400px" }} />
                                        </div>
                                    )}
                                </div>
                                <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
                                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                                    <span className="visually-hidden">Previous</span>
                                </button>
                                <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
                                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
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
