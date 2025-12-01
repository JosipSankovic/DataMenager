import { useContext, useEffect, useState } from "react";
import { ProjectContext } from "../../utils";
import { type ImageBase, ImagesService, OpenAPI, VersionsService } from "../../api";
import "./Dashboard.css";

export default function Dashboard() {
  const projectContext = useContext(ProjectContext);
  const [error, setError] = useState<string | null>(null);
  const [imagesInfo, setImagesInfo] = useState<Array<ImageBase>>([]);
  const [version_name,setVersionName] = useState("")
  const fetchImages = async () => {
      try {
        if (!projectContext?.project) return;
        const imgs_response = await ImagesService.getAllImagesGet(
          projectContext.project.id,
          0,
          10000
        );
        setImagesInfo(imgs_response);
      } catch (error) {
        console.error(error);
        setError("Cant fetch images");
      }
    };
  useEffect(() => {
    if(projectContext?.project)
     fetchImages();
    else
      setImagesInfo([])
  }, [projectContext?.project]);

  const getImgUrl = (url: string): string => {
    return `${OpenAPI.BASE}/images/serve_image?file_path=${encodeURIComponent(
      url
    )}`;
  };

  const onScanDataset=async()=>{
    try{
      if(!projectContext?.project) return
      const scanned_dataset = await ImagesService.scanDatasetImagesScanDatasetPost(projectContext.project.absolute_path,projectContext.project.id)
      fetchImages()
      console.log(scanned_dataset)
    }catch(error){
      console.error(error)
      setError("Failed to scan dataset")
    }
  }

  const onAddNewVersion=async()=>{
    try{
      if(!projectContext?.project) return
      if(version_name.trim().length==0) return
      const version_response = await VersionsService.addVersionVersionsPost({name:version_name,project_id:projectContext.project.id})
    }catch(error){
      console.error(error)
      setError("Failed to scan dataset")
    }
  }
  return (
    <>
      <div className="main-title">
        <h1>Dashboard</h1>
        <div className="search-bar">
          <span className="material-symbols-outlined">search</span>
          <input placeholder="Search images..." />
        </div>
      </div>
      <div className="main-content">
        <h2>Dataset annotations</h2>
        <button onClick={onScanDataset} className="btn-scan-dataset"><span>Apply differences</span></button>
        <div className="action-bar" style={{maxWidth:"30%"}}>
        <label className="input-label">
          <span className="label-text">Version name</span>
          <input 
            type="text" 
            className="text-input"
            value={version_name}
            onChange={(e) => setVersionName(e.target.value)}
          />
        </label>
        
        <button className="btn btn-primary" onClick={()=>onAddNewVersion()}>
          <span>Add version</span>
        </button>
      </div>

        {projectContext?.project?<div className="image-grid">
          {imagesInfo.map((img) => (
            <div key={img.id} className="image-card">
              <img
                src={getImgUrl(
                  `${projectContext?.project?.absolute_path}/${img.rel_path}`
                )}
                alt="Local file"
                className="w-full h-full object-cover"
                loading="lazy"
              />
              <div className="overlay">
                <p className="img-name">{img.rel_path}</p>
                <p>
                  Size: {img.width}x{img.height}
                </p>
                <p>Channels: {img.channels}</p>
              </div>
            </div>
          ))}
        </div>:null}
      </div>
    </>
  );
}
