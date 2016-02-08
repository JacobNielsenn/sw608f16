namespace spicams
{

    struct position
    {
        int x;
        int y;
    };

    position matching_method(cv::Mat, cv::Mat, int);
    position mid_of_target(int, int, int, int);
    cv::Mat read_image(std::string path_to_image);
}
