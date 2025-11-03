export const initialStore=()=>{
  return{
    message: null,
    todos: [
      {
        id: 1,
        title: "Make the bed",
        background: null,
      },
      {
        id: 2,
        title: "Do my homework",
        background: null,
      }
    ],
    token: sessionStorage.getItem("token") || null, // Token desde sessionStorage
    user: JSON.parse(sessionStorage.getItem("user")) || null, // Usuario desde sessionStorage
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
    case 'set_hello':
      return {
        ...store,
        message: action.payload
      };
      
    case 'add_task':
      const { id,  color } = action.payload
      return {
        ...store,
        todos: store.todos.map((todo) => (todo.id === id ? { ...todo, background: color } : todo))
      };
    
    case 'set_token':
      // Guardar en sessionStorage
      sessionStorage.setItem("token", action.payload.token);
      sessionStorage.setItem("user", JSON.stringify(action.payload.user));
      return {
        ...store,
        token: action.payload.token,
        user: action.payload.user
      };
    
    case 'logout':
      // Limpiar sessionStorage
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("user");
      return {
        ...store,
        token: null,
        user: null
      };
      
    default:
      throw Error('Unknown action.');
  }    
}