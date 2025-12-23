#pragma once
#include <string>
#include <iostream>
#include <nlohmann/json.hpp>
#include <opencv2/opencv.hpp>
#include <filesystem>
#include <fstream>
#include <algorithm>

struct Label{
    int class_id{0};
    std::string label;
    cv::Rect2f rect;
    std::vector<cv::Point2f> segment;
};
namespace fs = std::filesystem;
using json = nlohmann::json;
static int count = 0;
cv::Rect2f boundingRectFloat(const std::vector<cv::Point2f>& points);
//image augmentations
cv::Mat rotate_image(const cv::Mat& input, float angle);
cv::Mat change_brightness(const cv::Mat& input, float value);
//label augmentations
std::vector<Label> rotate_image_label(const std::vector<Label>& labels,int img_width,int img_height,int new_width,int new_height,double angle);

//label conversion
//yolov8
void save_as_yolo8(fs::path file_path, std::vector<Label> labels);
std::vector<Label> convert_to_yolo8(json& label_json,std::vector<std::string> label_names);

//other
void process_json(const std::vector<std::pair<std::string,std::string>> &data, const std::string& in_dir, const std::string& out_dir,std::vector<std::string> label_names);
std::tuple<std::vector<Label>,cv::Mat> augmentation_selector(fs::path file_path,std::vector<Label> labels,const std::string augmentation,float value);
cv::Mat imread_unicode(const fs::path& path, int flags = cv::IMREAD_COLOR);
//img_path,label_path
std::pair<fs::path,fs::path> aug_img_path(fs::path p_dir,fs::path file_name,std::string aug_type);
void augment_dataset(json data);
