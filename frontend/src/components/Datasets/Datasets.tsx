import { useContext, useState } from "react";
import { ProjectContext } from "../../utils";
import { DatasetService, type DatasetBase } from "../../api";
import "./Dataset.css"
export default function Datasets() {
  const projectContext = useContext(ProjectContext);
  const [datasets, setDatasets] = useState<Array<DatasetBase>>([]);
  const fetchDatasets = async () => {
    if (!projectContext?.project) return;
    try {
      const resp_datasets = await DatasetService.getAllDatasetAllGet(
        projectContext.project.id
      );
      setDatasets(resp_datasets);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <>
      <div className="main-title">
        <h1>Datasets</h1>
      </div>
      <div className="main-content">
        <h2>All datasets</h2>
        <button onClick={fetchDatasets} className="btn-scan-dataset">
          <span className="material-symbols-outlined">
download
</span><span>Fetch datasets</span>
        </button>
         <button onClick={fetchDatasets} className="btn-scan-dataset">
          <span className="material-symbols-outlined">add
</span><span>Add datasets</span>
        </button>
        <div className="datasets-content">
        {datasets.map((dataset) => (
         <Dataset dataset={dataset} key={dataset.id}/>
        ))}
        </div>
      </div>
    </>
  );
}


function Dataset({dataset}:{dataset:DatasetBase}){

    const createDataset=async()=>{
      const created_dataset = await DatasetService.createDatasetDatasetCreateFilesPost(dataset.id)
    }
    return(
         <div className="dataset-info">
            <span className="material-symbols-outlined" style={{fontSize:"50px"}}>perm_media</span>
            <div>
                <p className="dataset-title">{dataset.name}</p>
                <p className="dataset-description">{dataset.description}</p>
            </div>
            <p className="dataset-images">{dataset.size} Images</p>
            <button className="btn-scan-dataset" onClick={createDataset}><span>Create</span></button>
          </div>
    )
}