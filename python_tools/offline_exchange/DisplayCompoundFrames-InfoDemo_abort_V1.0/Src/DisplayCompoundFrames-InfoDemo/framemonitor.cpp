#include "framemonitor.h"
#include "frameext.h"

#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <time.h>

#include "satpext.h"
#include "frameid.h"
#include "frameformat.h"
#include "disparityconvertor.h"
#include "yuv2rgb.h"

#include "obstacleData.h"
#include "obstaclepainter.h"
#include "roadwaypainter.h"

const std::string & filepath(const std::string filename)
{
	time_t now;
	int unixTime = (int)time(&now);
	time_t tick = (time_t)unixTime;
	struct tm tm;
	char wtime[100];
	tm = *localtime(&tick);
	strftime(wtime, sizeof(wtime), "%Y-%m-%d_%H-%M-%S", &tm);
	printf("System time is :%s\n", wtime);
	static const std::string fileName = filename + "_" + wtime + ".csv";
	return fileName;
}


#ifdef _WIN64
//static const std::string ObstacleInfoFilePath = "../../ObstacleInfo_Logs.csv";
static const std::string ObstacleInfoFilePathN = "./ObstacleInfo_Logs";
static const std::string ObstacleInfoFilePath = filepath(ObstacleInfoFilePathN);
#else
static const std::string kHomeDir = getenv("HOME") ? getenv("HOME") : "/var";
static const std::string ObstacleInfoFilePathN = "/ObstacleInfo_Logs";
static const std::string ObstacleInfoFilePath = kHomeDir + filepath(ObstacleInfoFilePathN);
#endif

int64_t time_0;
int64_t time_x;

FrameMonitor::FrameMonitor()
    : mFrameReadyFlag(false),
      mDisparityFloatData(new float[1280 * 720]),
      mDisparityDistanceZ(new float[1280 * 720]),
      mRgbBuffer(new unsigned char[1280 * 720 * 3])
{
    // support gray or rgb
    mLeftMat.create(720/2, 1280/2, CV_8UC3);
    mRightMat.create(720/2, 1280/2, CV_8UC3);
    mDisparityMat.create(720/2, 1280/2, CV_8UC3);

	//add mCompoundMat for test
	mCompoundMat.create(720 / 2, 1280 / 2, CV_8UC3);

	//create a file to save ObstacleInfo
	FILE * fp = nullptr;
	fp = fopen(ObstacleInfoFilePath.data(), "wb+");
	if (!fp) {
		std::cout << ObstacleInfoFilePath << " file not open" << std::endl;
		return;
	}
	fprintf(fp, "time,stateLabel(CIPV),trackID,trackFrameNum,obstacleType,width,height,HMW,fuzzyCollisionTimeZ,longitudinalZ,speedOfLongitudinal,lateralX,speedOfLateral\n");
	fclose(fp);
}

void FrameMonitor::handleRawFrame(const RawImageFrame *rawFrame)
{
    processFrame(rawFrame, rawFrame->time);
}

void FrameMonitor::processFrame(const RawImageFrame *rawFrame,int64_t time)
{
    switch (rawFrame->frameId) {
    case FrameId::Disparity:
    {
        // only for FrameFormat::Disparity16, bitNum = 5
        std::lock_guard<std::mutex> lock(mMutex);
        loadFrameData2Mat(rawFrame, mDisparityMat);

//        std::cout << "update disparity mat" << std::endl;
        mFrameReadyFlag = true;
        mFrameReadyCond.notify_one();
    }
        break;
    case FrameId::CalibLeftCamera:
    {
        std::lock_guard<std::mutex> lock(mMutex);
        loadFrameData2Mat(rawFrame, mLeftMat);

//        std::cout << "update left mat" << std::endl;
        mFrameReadyFlag = true;
        mFrameReadyCond.notify_one();
    }
        break;
	//
	case FrameId::Compound:
	{
		char* extended = (char*)rawFrame + rawFrame->dataSize + sizeof(RawImageFrame);
		FrameDataExtHead *header = reinterpret_cast<FrameDataExtHead *>(extended);
		int blockNum = ((int *)header->data)[0];
		OutputObstacles *obsDataPack = (OutputObstacles *)(((int *)header->data) + 2);
		std::lock_guard<std::mutex> lock(mMutex);
		loadFrameData2Mat(rawFrame, mCompoundMat);
		mFrameReadyFlag = true;
		mFrameReadyCond.notify_one();

		//get ObstacleInfo,show them in window and save them to file.
		static int pic = 0;
		if (pic == 0) {
			time_0 = time;
		}
		else if (pic > 0) {
			time_x = time;
		}
		if (time_0 == time_x) {
			//exit(0);
			abort();
		}


		pic++;;
		for (int i = 0; i < blockNum; i++) {
			OutputObstacles *currentObstacle = &obsDataPack[i];
			int stateLabel = currentObstacle->stateLabel;
			int CIPV = stateLabel;
			int trackID = currentObstacle->trackId;
			int trackFrameNum = currentObstacle->trackFrameNum;
			int obstacleType = currentObstacle->obstacleType;
			float real3DRightX = currentObstacle->real3DRightX;
			float real3DLeftX = currentObstacle->real3DLeftX;
			float width = fabs(real3DRightX - real3DLeftX);
			float real3DLowY = currentObstacle->real3DLowY;
			float real3DUpY = currentObstacle->real3DUpY;
			float height = fabs(real3DLowY - real3DUpY);
			float HMW = currentObstacle->fuzzy3DWidth;
			float fuzzyCollisionTimeZ = currentObstacle->fuzzyCollisionTimeZ; //TTC
			float longitudinalZ = currentObstacle->avgDistanceZ;
			float speedOfLongitudinal = currentObstacle->fuzzyRelativeSpeedZ;
			float lateralX = currentObstacle->real3DCenterX;
			float speedOfLateral = currentObstacle->fuzzyRelativeSpeedCenterX;
			if (pic != 0) {
				// get the Obstacle data, and save one to file for verification
				FILE * fp = nullptr;
				fp = fopen(ObstacleInfoFilePath.data(), "ab+");
				if (!fp) {
					std::cout << ObstacleInfoFilePath << " file not open" << std::endl;
					return;
				}
				fprintf(fp, "%lld,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f,%f,%f\n", time, stateLabel, trackID, trackFrameNum, obstacleType, width, height, HMW, fuzzyCollisionTimeZ, longitudinalZ, speedOfLongitudinal, lateralX, speedOfLateral);
				fclose(fp);
			}
			else
				printf("Finish!! 'obstacle_Logs.txt' has been created!\n");
			printf("time:%lld  stateLabel:%d  ID:%d\tTN:%d  Type:%d\tW:%f\tH:%f\tHMW:%f\tTTC:%f\tDZ:%f\tVZ:%f\tDX:%f\tVX:%f\n", time, stateLabel, trackID, trackFrameNum, obstacleType, width, height, HMW, fuzzyCollisionTimeZ, longitudinalZ, speedOfLongitudinal, lateralX, speedOfLateral);
		}
		printf("\n");

	}
	break;
    }
}

void FrameMonitor::waitForFrames()
{
    std::unique_lock<std::mutex> lock(mMutex);
    mFrameReadyCond.wait_for(lock, std::chrono::milliseconds(240), [this]{
        return mFrameReadyFlag;
    });

    mFrameReadyFlag = false;
}

cv::Mat FrameMonitor::getFrameMat(int frameId)
{
    std::lock_guard<std::mutex> lock(mMutex);

    switch (frameId) {
    case FrameId::CalibRightCamera:
        return mRightMat.clone();
    case FrameId::Disparity:
        return mDisparityMat.clone();
	case FrameId::Compound:
		return mCompoundMat.clone();
    default:
        return mLeftMat.clone();
    }
}

void FrameMonitor::loadFrameData2Mat(const RawImageFrame *frameData, cv::Mat &dstMat)
{
    int width = frameData->width;
    int height = frameData->height;
    const unsigned char *imageData = frameData->image;
	//
	char* extended = (char*)frameData + frameData->dataSize + sizeof(RawImageFrame);
	FrameDataExtHead *header = reinterpret_cast<FrameDataExtHead *>(extended);

    switch (frameData->format) {
    case FrameFormat::Disparity16:
    {
//        DisparityConvertor::convertDisparity2FloatFormat(imageData, width, height, 5, mDisparityFloatData.get());
//        DisparityConvertor::convertDisparity2RGB(mDisparityFloatData.get(), width, height, 0, 45, mRgbBuffer.get());
//        cv::Mat dispMat(height, width, CV_8UC3, mRgbBuffer.get());
//        cv::resize(dispMat, dstMat, dstMat.size());

        cv::Mat dispMat(height, width, CV_16U, (void*)imageData);
        cv::resize(dispMat, dstMat, dstMat.size());
        cv::normalize(dstMat, dstMat, 0, 255, cv::NORM_MINMAX, CV_8U);
    }
        break;
    case FrameFormat::Gray:
    {
		//default
        //cv::Mat grayMat(height, width, CV_8UC1, (void*)imageData);
        //cv::resize(grayMat, dstMat, dstMat.size());

		//show compound Frame
		RoadwayPainter::imageGrayToRGB(imageData, (unsigned char*)mRgbBuffer.get(), width, height);
		ObstaclePainter::paintObstacle(header->data, mRgbBuffer.get(), width, height, true, false);
		cv::Mat compoundCustomMat(height, width, CV_8UC3, mRgbBuffer.get());
		cv::resize(compoundCustomMat, dstMat, dstMat.size());
		cv::cvtColor(dstMat, dstMat, CV_RGB2BGR);
    }
        break;
    case FrameFormat::YUV422:
    {
        YuvToRGB::YCbYCr2Rgb(imageData, (char *)mRgbBuffer.get(), width, height);
        cv::Mat yuv422Mat(height, width, CV_8UC3, mRgbBuffer.get());
        cv::resize(yuv422Mat, dstMat, dstMat.size());
        cv::cvtColor(dstMat, dstMat, CV_RGB2BGR);
    }
        break;
    case FrameFormat::YUV422Plannar:
    {
        YuvToRGB::YCbYCrPlannar2Rgb(imageData, (char *)mRgbBuffer.get(), width, height);
        cv::Mat yuv422PlannarMat(height, width, CV_8UC3, mRgbBuffer.get());
        cv::resize(yuv422PlannarMat, dstMat, dstMat.size());
        cv::cvtColor(dstMat, dstMat, CV_RGB2BGR);
    }
        break;
    }
}
