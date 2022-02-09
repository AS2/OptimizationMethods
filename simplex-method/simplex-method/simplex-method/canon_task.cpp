#include <iostream>
#include <sstream>
#include <algorithm>
#include <fstream>

#include "canon_task.h"

const std::string WHITESPACE = " \n\r\t\f\v";

std::string ltrim(const std::string& s)
{
  size_t start = s.find_first_not_of(WHITESPACE);
  return (start == std::string::npos) ? "" : s.substr(start);
}

std::string rtrim(const std::string& s)
{
  size_t end = s.find_last_not_of(WHITESPACE);
  return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::string trim(const std::string& s) {
  return rtrim(ltrim(s));
}

std::vector<std::string> split(const std::string& s, char delim) {
  std::vector<std::string> elems;
  std::stringstream ss(s);
  std::string item;

  while (std::getline(ss, item, delim)) {
    elems.push_back(trim(item));
  }

  return elems;
}

canon_task::canon_task(std::string& fileName) {
  std::vector<std::string> TAGS_NAMES = {"n_size", "min_coef", "min_freeValue", "equal", "more_equal", "less_equal", "not_neg_indexes"};

  std::ifstream fileStream(fileName);

  if (!fileStream.is_open()) {
    errorSingleton::GetInstance().UpdateMessage(true, "Can't open file");
    return;
  }
  B = 0;

  std::string line;
  std::vector<std::string> parts;
  bool wasSize = false, wasNotNegIndexes = false;
  while (getline(fileStream, line)) {
    parts = split(line, '=');
    if (parts.size() != 2) {
      errorSingleton::GetInstance().UpdateMessage(true, "Bad string in resource file : uncorrect delimeter between tag word and values");
      return;
    }


    if (parts[0] == TAGS_NAMES[0]) {  // "n_size"
      wasSize = true;
      originalN = N = atoi(parts[1].c_str());
    }
    else if (wasSize && !wasNotNegIndexes && parts[0] == TAGS_NAMES[1]) { // "min_coef"
      std::vector<std::string> coefs = split(parts[1], ' ');
      if (coefs.size() != N) {
        errorSingleton::GetInstance().UpdateMessage(true, "Bad 'min_coef' arguments : coefs count and 'n_size' must be the same!");
        return;
      }
      for_each(coefs.begin(), coefs.end(), [&](std::string coef) { c.push_back(atof(coef.c_str())); });
    }
    else if (wasSize && !wasNotNegIndexes && parts[0] == TAGS_NAMES[2]) { // "min_freeValue"
      std::vector<std::string> value = split(parts[1], ' ');
      if (value.size() != 1) {
        errorSingleton::GetInstance().UpdateMessage(true, "Bad 'min_freeValue' arguments : there must be only one value!");
        return;
      }
      v = atof(value[0].c_str());
    }
    else if (wasSize && !wasNotNegIndexes && parts[0] == TAGS_NAMES[3]) { // "equal"
      std::vector<std::string> equalCoefs = split(parts[1], ' ');
      if (equalCoefs.size() != N + 1) {
        errorSingleton::GetInstance().UpdateMessage(true, "Bad 'equal' #" + std::to_string(B) + " arguments : coefs count must be for one more tha 'n_size'! (last one coef - is free coef)");
        return;
      }
      // make 'less_equal'
      A.push_back({});
      for (int i = 0; i < N; i++)
        A[B].push_back(atof(equalCoefs[i].c_str()));
      b.push_back(atof(equalCoefs[N].c_str()));
      B++;

      // make 'more_equal'
      A.push_back({});
      for (int i = 0; i < N; i++)
        A[B].push_back(-1 * atof(equalCoefs[i].c_str()));
      b.push_back(-1 * atof(equalCoefs[N].c_str()));
      B++;
    }
    else if (wasSize && !wasNotNegIndexes && parts[0] == TAGS_NAMES[4]) { // "more_equal"
      std::vector<std::string> equalCoefs = split(parts[1], ' ');
      if (equalCoefs.size() != N + 1) {
        errorSingleton::GetInstance().UpdateMessage(true, "Bad 'more_equal' arguments : coefs count must be for one more tha 'n_size'! (last one coef - is free coef)");
        return;
      }
      A.push_back({});
      for (int i = 0; i < N; i++)
        A[B].push_back(-1 * atof(equalCoefs[i].c_str()));
      b.push_back(-1 * atof(equalCoefs[N].c_str()));
      B++;
    }
    else if (wasSize && !wasNotNegIndexes && parts[0] == TAGS_NAMES[5]) { // "less_equal"
      std::vector<std::string> equalCoefs = split(parts[1], ' ');
      if (equalCoefs.size() != N + 1) {
        errorSingleton::GetInstance().UpdateMessage(true, "Bad 'less_equal' arguments : coefs count must be for one more tha 'n_size'! (last one coef - is free coef)");
        return;
      }
      A.push_back({});
      for (int i = 0; i < N; i++)
        A[B].push_back(atof(equalCoefs[i].c_str()));
      b.push_back(atof(equalCoefs[N].c_str()));
      B++;
    }
    else if (wasSize && !wasNotNegIndexes && parts[0] == TAGS_NAMES[6]) { // "not_neg_indexes"
      wasNotNegIndexes = true;
      std::vector<std::string> indexes = split(parts[1], ' ');
      if (indexes.size() > N) {
        errorSingleton::GetInstance().UpdateMessage(true, "Bad 'not_neg_indexes' arguments : indexes count and 'n_size' must be the same!");
        return;
      }

      if (N - indexes.size() != 0) {
        fakesValuesIndexes.reserve(N - indexes.size());

        for (size_t i = 0; i < originalN; i++) {
          int j;
          for (j = 0; j < indexes.size(); j++) {
            if (i == atoi(indexes[j].c_str()))
              break;
          }
          // if value could be not negative
          if (j == indexes.size()) {
            for (auto& an_equal : A)
              an_equal.push_back(-1 * an_equal[i]);
            c.push_back(-1 * c[i]);
            fakesValuesIndexes.push_back({ i, i, originalN + i });
            N++;
          }
        }
      }
    }
  }

  fileStream.close();
}

// ÏÎÑËÅ ÍÀÉÄÅÍÍÎÃÎ ÐÅØÅÍÈß ÊÀÊÈÌ ËÈÁÎ ÌÅÒÎÄÎÌ, ÏÐÎÑÓÍÜ ÝÒÎ ÐÅØÅÍÈÅ ÑÞÄÀ, ×ÒÎÁ ÏÎËÓ×ÈÒÜ ÓÆÅ ÐÅÙÅÍÈÅ ÈÑÕÎÄÍÎÉ ÇÀÄÀ×È
std::vector<double> canon_task::vectorConvolutional(std::vector<double>& vectorToConvolute) {
  std::vector<double> newVec(originalN);
  return newVec;
}

void canon_task::print() {
  // BUILD TARGET FUNC
  std::string targetfunc = "max: z = " + std::to_string(v);
  for (int i = 0; i < c.size(); i++)
    targetfunc += " + " + std::to_string(c[i]) + " * x" + std::to_string(i + 1);
  std::cout << targetfunc << "\n";

  // BUILD EXPRESSIONS
  for (int i = 0; i < B; i++) {
    std::string expr = "x" + std::to_string(i + 1 + N) + " = " + std::to_string(b[i]);
    for (int j = 0; j < A[i].size(); j++)
      expr += " - " + std::to_string(A[i][j]) + " * x" + std::to_string(j + 1);
    std::cout << expr << "\n";
  }

  // BUILD VARIABLES
  std::string expr = "";
  for (int i = 0; i < N + B; i++) {
    expr += "x" + std::to_string(i + 1);
    if (i + 1 != N + B)
      expr += ", ";
  }
  std::cout << expr + " >= 0" << "\n";
}
