import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import "./ShowFolderImages.css"
import { ImagesService, OpenAPI } from '../../api';
import { ProjectContext } from '../../utils';



const DataIngestion = () => {
  const [directoryPath, setDirectoryPath] = useState("D:/Ministarstvo/ministarstvo_dataset");
  const [images,setImages] = useState<Array<string>>([])
  const [page,setPage] = useState(1)
  const [scannedPath,setScannedPath]= useState("")
  const projectContext = useContext(ProjectContext)

  const fetchImages=async ()=>{
    try{
    setScannedPath(directoryPath)
    const res_images = await ImagesService.getFolderImagesImagesFolderImagesGet(directoryPath,page)
    setImages(res_images)
    }catch(error){
        console.error(error)
    }
  }
  const getImgUrl=useCallback((url:string):string=>{
    return `${OpenAPI.BASE}/images/serve_image?file_path=${encodeURIComponent(url)}`;
  },[images])

  const removeImage=(img_name:string)=>{
    setImages(prev=>prev.filter((img)=>img!=img_name))
  }

  const addImagesToProject=async()=>{
    if(!projectContext?.project) return
    const response = await ImagesService.addImgToProjectImagesAddImgsToProjectPost(scannedPath,projectContext.project.id,images)
  }
  return (
    <main className="main-container">
      {/* Page Heading */}
      <div className="page-heading">
        <h1 className="page-title">Data Ingestion</h1>
      </div>

      {/* Action Bar */}
      <div className="action-bar">
        <label className="input-label">
          <span className="label-text">Local Directory Path</span>
          <input 
            type="text" 
            className="text-input"
            value={directoryPath}
            onChange={(e) => setDirectoryPath(e.target.value)}
          />
        </label>
        
        <button className="btn btn-primary" onClick={()=>fetchImages()}>
          <span>Scan Directory</span>
        </button>
      </div>
        <div  className="meta-data">
        <p>Showing 20 of {images.length} images</p>
        {images.length!=0?<button onClick={addImagesToProject} >Add to project dataset</button>:null}
        </div>
      {/* Meta Text */}
    
      {/* Image Grid */}
      <div className="image-grid">
        {images.map((img,idx) => (
          <div key={idx} className="image-card">
            <img 
              src={getImgUrl(`${scannedPath}/${img}`)}
              alt="Local file"
              className="w-full h-full object-cover"
              loading="lazy"
            />
            
            {/* Overlay and controls (Visible on CSS Hover) */}
            <div className="overlay">
              <button 
                className="btn btn-close" 
                title="Exclude image"
                onClick={() => removeImage(img)}
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
};

export default DataIngestion;