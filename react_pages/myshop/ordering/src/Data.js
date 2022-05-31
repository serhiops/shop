import DataList from "./components/DataList";

const Data = (data) => {
  return (
    <div >
      <DataList {... data}/>
    </div>
  );
}

export default Data;
