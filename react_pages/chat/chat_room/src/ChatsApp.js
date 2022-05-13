import Chats from "./components/Chats";


function ChatsApp(data) {
  return (
    <div>
      <Chats {... data}/>
    </div>
  );
}

export default ChatsApp;
