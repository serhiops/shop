import Product from "./components/Product";

const ProductApp = (data) => {
  return (
    <div>
      <Product {...data}/>
    </div>
  );
}

export default ProductApp;
