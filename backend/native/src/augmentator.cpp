#include "augmentator.hpp"


cv::Rect2f boundingRectFloat(const std::vector<cv::Point2f>& points) {
    if (points.empty()) return cv::Rect2f(0, 0, 0, 0);

    float min_x = points[0].x;
    float max_x = points[0].x;
    float min_y = points[0].y;
    float max_y = points[0].y;

    for (const auto& pt : points) {
        if (pt.x < min_x) min_x = pt.x;
        if (pt.x > max_x) max_x = pt.x;
        if (pt.y < min_y) min_y = pt.y;
        if (pt.y > max_y) max_y = pt.y;
    }

    return cv::Rect2f(min_x, min_y, max_x - min_x, max_y - min_y);
}
std::pair<fs::path,fs::path> aug_img_path(fs::path p_dir, fs::path file_name, std::string aug_type)
{
    // Pretpostavimo da je file_name npr. "frame_001.jpg"
    fs::path original_path(file_name);

    // 1. Dohvati samo ime bez ekstenzije (npr. "frame_001")
    std::string basic_name = original_path.stem().string();

    // 2. Dohvati originalnu ekstenziju (npr. ".jpg") - ili hardkodiraj ".jpg" ako želiš
    std::string ext = original_path.extension().string();

    // 3. Složi novi naziv (frame_001 + _ + rotation + .jpg)
    std::string new_img_filename = basic_name + "_" + aug_type + std::to_string(++count) + ext;
    std::string new_lbl_filename = basic_name + "_" + aug_type + std::to_string(count) + ".txt";

    // 4. Spoji s direktorijem
    fs::path full_img_save_path = p_dir / new_img_filename;
    fs::path full_lbl_save_path = p_dir / new_lbl_filename;
    
    return {full_img_save_path,full_lbl_save_path};
}
cv::Mat imread_unicode(const fs::path &path, int flags)
{
    // 1. Provjera postoji li datoteka
    if (!fs::exists(path))
    {
        std::cerr << "Datoteka ne postoji: " << path << std::endl;
        return cv::Mat();
    }

    // 2. Otvaranje datoteke pomoću binarnog streama (ovo podržava Unicode na Windowsima)
#ifdef _WIN32
    // Na windowsima koristimo wstring (wide string) za putanju
    std::ifstream file(path.wstring(), std::ios::binary);
#else
    std::ifstream file(path.string(), std::ios::binary);
#endif

    if (!file.good())
    {
        std::cerr << "Ne mogu otvoriti datoteku (stream error)." << std::endl;
        return cv::Mat();
    }

    // 3. Učitavanje bajtova u vector
    // Pomičemo se na kraj da saznamo veličinu
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    std::vector<char> buffer(fileSize);
    file.read(buffer.data(), fileSize);

    // 4. Dekodiranje slike iz memorije
    // cv::imdecode čita sliku iz niza bajtova (RAW data)
    return cv::imdecode(cv::Mat(buffer), flags);
}
cv::Mat rotate_image(const cv::Mat &input, float angle)
{
    if (input.empty()) return cv::Mat();

    cv::Mat output;

    // FIX: Align special cases with OpenCV standard (Positive = Counter-Clockwise)
    
    // Case 1: 90 degrees (CCW)
    if (abs(angle - 90) < 0.1 || abs(angle - (-270)) < 0.1) 
    {
        // Was CLOCKWISE, must be COUNTERCLOCKWISE to match getRotationMatrix2D(90)
        cv::rotate(input, output, cv::ROTATE_90_COUNTERCLOCKWISE); 
    }
    // Case 2: -90 degrees (or 270 CCW)
    else if (abs(angle - (-90)) < 0.1 || abs(angle - 270) < 0.1) 
    {
        // Was COUNTERCLOCKWISE, must be CLOCKWISE to match getRotationMatrix2D(-90)
        cv::rotate(input, output, cv::ROTATE_90_CLOCKWISE); 
    }
    // Case 3: 180 degrees
    else if (abs(angle - 180) < 0.1 || abs(angle - (-180)) < 0.1) 
    {
        cv::rotate(input, output, cv::ROTATE_180);
    }
    else
    {
        // General case (45, 30, etc.) uses getRotationMatrix2D
        // This is naturally Counter-Clockwise for positive angles.
        cv::Point2f center((input.cols - 1) / 2.0f, (input.rows - 1) / 2.0f);
        cv::Mat rot_mat = cv::getRotationMatrix2D(center, angle, 1.0);
        cv::warpAffine(input, output, rot_mat, input.size());
    }

    return output;
}
cv::Mat change_brightness(const cv::Mat &input, float value)
{
    // Ako je ulazna slika prazna, vratimo praznu sliku
    if (input.empty())
    {
        return cv::Mat();
    }
    cv::Mat output;
    // input.convertTo(output, rtype, alpha, beta);
    // Formula: output = input * alpha + beta
    // alpha (1.0) = kontrast (ne mijenjamo ga)
    // beta (value) = svjetlina (dodajemo ili oduzimamo)
    // -1 znači da izlazna slika ima isti tip podataka kao ulazna (npr. CV_8UC3)
    input.convertTo(output, -1, 1.0, value);

    return output;
}
std::vector<Label> rotate_image_label(const std::vector<Label>& labels,int img_width,int img_height,int new_width,int new_height,double angle) {
    
    std::vector<Label> r_labels;
    
  
    cv::Point2f old_center((img_width - 1) / 2.0f, (img_height - 1) / 2.0f);
    cv::Point2f new_center((new_width - 1) / 2.0f, (new_height - 1) / 2.0f);
    // 2. Get the Rotation Matrix (Rotates around OLD center)
    cv::Mat rotation_M = cv::getRotationMatrix2D(old_center, angle, 1.0);

    //We shift the matrix so the points align with the NEW center
    rotation_M.at<double>(0, 2) += (new_center.x - old_center.x);
    rotation_M.at<double>(1, 2) += (new_center.y - old_center.y);
    
    for (const auto& label : labels) {
        std::vector<cv::Point2f> new_corners;
        std::vector<cv::Point2f> new_segment_px;
        Label n_label;
        n_label.class_id = label.class_id;
        n_label.label = label.label;

        float x = label.rect.x * img_width;
        float y = label.rect.y * img_height;
        float w = label.rect.width * img_width;
        float h = label.rect.height * img_height;

        std::vector<cv::Point2f> corners = {
            cv::Point2f(x, y),
            cv::Point2f(x + w, y),
            cv::Point2f(x + w, y + h),
            cv::Point2f(x, y + h)
        };
        cv::transform(corners,new_corners,rotation_M);
        std::vector<cv::Point2f> segment_px;
        if (!label.segment.empty()) {
            for (const auto& p : label.segment) {
                segment_px.push_back(cv::Point2f(p.x * img_width, p.y * img_height));
            }
            cv::transform(segment_px,new_segment_px,rotation_M);

        }
        if (!new_segment_px.empty()) {
            for (auto& p : new_segment_px) {
                n_label.segment.push_back({p.x / new_width, p.y / new_height});
            }
            cv::Rect2f px_rect = boundingRectFloat(new_segment_px);
            n_label.rect.x = px_rect.x / new_width;
            n_label.rect.y = px_rect.y / new_height;
            n_label.rect.width = px_rect.width / new_width;
            n_label.rect.height = px_rect.height / new_height;
        } 
        else {
            cv::Rect2f px_rect = boundingRectFloat(new_corners);
            n_label.rect.x = px_rect.x / new_width;
            n_label.rect.y = px_rect.y / new_height;
            n_label.rect.width = px_rect.width / new_width;
            n_label.rect.height = px_rect.height / new_height;
        }
        
        n_label.rect.x = std::max(0.0f, n_label.rect.x);
        n_label.rect.y = std::max(0.0f, n_label.rect.y);
        if (n_label.rect.x + n_label.rect.width > 1.0f) n_label.rect.width = 1.0f - n_label.rect.x;
        if (n_label.rect.y + n_label.rect.height > 1.0f) n_label.rect.height = 1.0f - n_label.rect.y;
        r_labels.push_back(n_label);
    }
    return r_labels;
}
void process_json(const std::vector<std::pair<std::string,std::string>> &data, const std::string &in_dir, const std::string &out_dir,std::vector<std::string> label_names)
{
    fs::path p_dir = in_dir;
    fs::path o_dir = out_dir;

    try
    {
        // go trough all train images
        for (const auto& image_pair : data)
        {
            auto image_info = json::parse(image_pair.first);
            auto image_labels = json::parse(image_pair.second);
            fs::path file_name = image_info["rel_path"];
            fs::path file_path = p_dir / file_name;
            fs::path base_name = file_path.stem();
            std::vector<Label> lbls=convert_to_yolo8(image_labels,label_names);
            const auto &augmetations_type = image_info["augmentations"];
            // get all augmentations with their values
            for (const auto &[key, values] : augmetations_type.items())
            {
                if (!augmetations_type[key].is_array())
                    continue;
                for (const auto &item : values)
                {
                    if (item.is_number())
                    {
                        std::tuple<std::vector<Label>, cv::Mat> augmented_result = augmentation_selector(file_path,lbls, key, item.get<float>());
                        if (std::get<0>(augmented_result).size()==0)
                            continue;
                        if (std::get<1>(augmented_result).empty())
                            continue;
                        auto full_paths = aug_img_path(o_dir, file_name, key);
                        cv::imwrite(full_paths.first.string(), std::get<1>(augmented_result));
                        save_as_yolo8(full_paths.second,std::get<0>(augmented_result));

                    }
                }
                // augment images
            }
        }
    }
    catch (const json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
    }
}
void augment_dataset(json data, fs::path dir_path)
{
    for (const auto &image_info : data)
    {
        fs::path file_name = image_info["rel_path"];
        fs::path file_path = dir_path / file_name;
        const auto &aug_type = image_info["augmentations"];

        for (const auto &[key, values] : aug_type.items())
        {
            if (!aug_type[key].is_array())
                continue;
            for (const auto &item : values)
            {
                if (!item.is_number())
                    continue;
            }
        }
    }
}
void save_as_yolo8(fs::path file_path, std::vector<Label> labels)
{
    std::ofstream label_file(file_path);
    if (!label_file.is_open())
    {
        std::cerr << "Cant create " << file_path << " file \n";
        return;
    }
    for (const auto &label : labels)
    {
        label_file<<label.class_id;
        
        if(label.rect.width!=0&&label.rect.height!=0){
            float x_center = label.rect.x+label.rect.width/2.0;
            float y_center = label.rect.y+label.rect.height/2.0;
            float width = label.rect.width;
            float height = label.rect.height;
            label_file<<" "<<x_center<<" "<<y_center<<" "<<width<<" "<<height;
        }else{
        for(const auto& p:label.segment){
                    label_file<<" "<<p.x<<" "<<p.y;
                }
        }
        label_file<<"\n";
    }
}
std::vector<Label> convert_to_yolo8(json& label_json,std::vector<std::string> label_names){
    json shapes = label_json["shapes"];
    float image_width = label_json["imageWidth"];
    float image_height = label_json["imageHeight"];
    std::vector<Label> f_labels;
    for(const auto& shape:shapes){
        Label f_label;
        f_label.label = shape["label"];
        auto it = std::find(label_names.begin(),label_names.end(),f_label.label);
        if(it==label_names.end()){
            f_label.class_id = -1;
        }else{
            f_label.class_id = static_cast<int>(std::distance(label_names.begin(),it));
        }
        if(shape["shape_type"]=="rectangle"){
            f_label.rect.x = shape["points"][0][0].get<float>()/image_width;
            f_label.rect.y = shape["points"][0][1].get<float>()/image_height;
            f_label.rect.width = (shape["points"][1][0].get<float>()-shape["points"][0][0].get<float>())/image_width;
            f_label.rect.height = (shape["points"][2][1].get<float>()-shape["points"][0][1].get<float>())/image_height;
        }
        else if(shape["shape_type"]=="polygon"){
            for(const auto& point:shape["points"]){
                cv::Point2f p;
                if(!point[0].is_number())continue;
                p.x = point[0].get<float>()/image_width;
                p.y = point[1].get<float>()/image_height;
                f_label.segment.push_back(p);
        }
        }
        f_labels.push_back(f_label);
    }
    return f_labels;
}
std::tuple<std::vector<Label>, cv::Mat> augmentation_selector(fs::path file_path,std::vector<Label> labels, const std::string augmentation, float value)
{
    cv::Mat image = imread_unicode(file_path);
    int img_width = image.cols;
    int img_height = image.rows;
    if (image.empty())
        return std::tuple<std::vector<Label>, cv::Mat>({}, cv::Mat());
    if (augmentation == "rotation"){
        auto new_image =  rotate_image(image, value);
        int new_img_width = new_image.cols;
        int new_img_height = new_image.rows;
        std::vector<Label> new_labels=rotate_image_label(labels,img_width,img_height,new_img_width,new_img_height,value);
        return std::tuple<std::vector<Label>, cv::Mat>(new_labels,new_image);

    }
    else if (augmentation == "brightness")
        return std::tuple<std::vector<Label>, cv::Mat>(labels, change_brightness(image, value));

    return std::tuple<std::vector<Label>, cv::Mat>({}, cv::Mat());
}
