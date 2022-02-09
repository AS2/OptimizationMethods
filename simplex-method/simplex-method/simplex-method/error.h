#pragma once
#include <string>

class errorSingleton {
private:
  bool errorCode;
  std::string errorMessage;

  errorSingleton() {
    errorCode = false;
  }
public:
  void UpdateMessage(bool errCode, std::string errMsg) {
    errorCode = errCode;
    errorMessage = errMsg;
  }

  bool isError() {
    return errorCode;
  }

  std::string GetMessage() {
    return errorMessage;
  }

  static errorSingleton& GetInstance() {
    static errorSingleton error;
    return error;
  }
};