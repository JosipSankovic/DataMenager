import { useContext, useEffect, useState } from "react";
import { ProjectContext } from "../../utils";
import { type ImageBase, ImagesService, OpenAPI } from "../../api";
import "./Dashboard.css";
export default function Dashboard() {
  const projectContext = useContext(ProjectContext);
  const [error, setError] = useState<string | null>(null);
  const [imagesInfo, setImagesInfo] = useState<Array<ImageBase>>([]);
  useEffect(() => {
    const fetchImages = async () => {
      try {
        if (!projectContext?.project) return;
        const imgs_response = await ImagesService.getAllImagesGet(
          projectContext.project.id,
          0,
          1000
        );
        setImagesInfo(imgs_response);
      } catch (error) {
        console.error(error);
        setError("Cant fetch images");
      }
    };
    fetchImages();
  }, [projectContext?.project]);

  const getImgUrl = (url: string): string => {
    return `${OpenAPI.BASE}/images/serve_image?file_path=${encodeURIComponent(
      url
    )}`;
  };
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
        <div className="image-grid">
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
        </div>
      </div>
    </>
  );
}
