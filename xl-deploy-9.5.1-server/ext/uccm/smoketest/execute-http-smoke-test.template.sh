#!/bin/sh


START_DELAY_SECS=${startDelay}

if [ $START_DELAY_SECS -ne 0 ]; then
echo Waiting $START_DELAY_SECS seconds
sleep $START_DELAY_SECS
fi

MAX_RETRIES=${maxRetries}
RETRY_INTERVAL_SECS=${retryWaitInterval}

for i in `seq 1 $MAX_RETRIES`
do
RESPONSE_FILE=http-response.$$
rm -f $RESPONSE_FILE

echo "wget --timeout=30 --no-check-certificate -O $RESPONSE_FILE ${target_url}"

wget --timeout=30 --no-check-certificate -O $RESPONSE_FILE ${target_url}

WGET_EXIT_CODE=$?
if [ $WGET_EXIT_CODE -eq 0 ]; then
break
fi
sleep $RETRY_INTERVAL_SECS
done

if [ $WGET_EXIT_CODE -ne 0 ]; then
echo ERROR: URL '${target_url}' returned non-200 response code
exit $WGET_EXIT_CODE
fi

echo Making sure response contains: "${expectedResponseText}"
grep "${expectedResponseText}" $RESPONSE_FILE

SEARCH_EXIT_CODE=$?

if [ $SEARCH_EXIT_CODE -ne 0 ]; then
echo ERROR: Response body did not contain: "${expectedResponseText}"
exit $SEARCH_EXIT_CODE
fi



