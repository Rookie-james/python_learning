#include <iostream>
#include <opencv2/highgui.hpp>

#include "stereocamera.h"
#include "framemonitor.h"
#include "frameid.h"
#include "taskiddef.h"

#include <time.h>
/**
 * @brief main
 * @note the sdk base on qt
 * @note on linux x86 desktop platform, there are some problems to use opencv_highgui module without qt event loop
 * @note here, calling functions of highgui in qt event loop is correct, called by invokeInLoopThread() by class StereoCamera
 */

int main(int argc, char *argv[])
{
    StereoCamera *camera = StereoCamera::connect("192.168.1.251");
    std::unique_ptr<FrameMonitor> frameMonitor(new FrameMonitor);

    camera->enableTasks(TaskId::DisplayTask | TaskId::ObstacleTask);
    camera->requestFrame(frameMonitor.get(), FrameId::Compound);

    std::function<int()> draw_func = [&frameMonitor]() -> int {
		cv::Mat compoundFrame = frameMonitor->getFrameMat(FrameId::Compound);
		if (!compoundFrame.empty()) {
			cv::imshow("Compound", compoundFrame);
		}

        return cv::waitKey(80);
    };

    camera->invokeInLoopThread([]{
		cv::namedWindow("Compound");
    });

    // main thread loop for drawing images
    while (true) {
        frameMonitor->waitForFrames();  // wait for frames ready

        int key = 0;
        camera->invokeInLoopThread([&key, &draw_func]{
            key = draw_func();
        });

        if (key == 27) {
            // press Esc to close
            break;
        }
    }

    camera->invokeInLoopThread([]{
        cv::destroyAllWindows();
    });

    return 0;
}

