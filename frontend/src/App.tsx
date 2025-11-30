import { OpenAPI } from './api'
import './App.css'
import ShowFolderImages from './components/ShowFolderImages/ShowFolderImages'

function App() {
  OpenAPI.BASE = "http://localhost:8000"
  
  return (
    <ShowFolderImages />
  )
}

export default App
