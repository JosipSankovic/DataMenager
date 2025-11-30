import { OpenAPI, type ProjectBase } from './api'
import './App.css'
import Layout from './components/Layout/Layout'
import ShowFolderImages from './components/ShowFolderImages/ShowFolderImages'
import { BrowserRouter,Route,Routes } from 'react-router'
import { ProjectContext } from './utils'
import { useState } from 'react'
import Dashboard from './components/Dashboard/Dashboard'

function App() {
  OpenAPI.BASE = "http://localhost:8000"
  const [project,setProject] = useState<ProjectBase|null>(null)
  return (
    <ProjectContext.Provider value={{project:project,setProject:setProject}}>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />} >
        <Route path='/' index element={<Dashboard />} />
        <Route path ="/addimages" index element={<ShowFolderImages/>} />
        </Route>
      </Routes>
    </BrowserRouter>
    </ProjectContext.Provider>
  )
}

export default App
