# Problem Statement

As a new SRE for the team that manages a payment service for an internet company, how would you establish the SLA for your services?
Services:
- payment-request: Handles requests for orchestrating a payment using credit card
- payment-history: Management payment requests history
- payment-gateway: Initiates a payment request with PSP ( payment service provider for e.g Adyen )
---

# Solution Approach 

### Context Setup

In my experience establishing SLA involves multiple parties like product owners, business stakeholder, technical team etc, 
which help in defining right objectives expected from services in terms customer expectations, compliances, release velocity 
error budgets etc.

As a SRE, I will start focusing on the determining SLI’s to gain the insight about my services by collecting right set of metrics, that represents the performance and reliability of my service. These metrics should directly relates to business objectives and user experience as discussed above.


Based on SLI’s, I will try to set specific SLO’s and create SLA agreement and review based on my learning about system behavior. I will try to start lean with minimum expectation and optimized the platform based on metrics feedback and system load.
  

### Common Approach ( Suggested Guideline like google SRE ):
 
1. Define SLI ( Identity Key Metrics )
    ```text
        - Availability : measure number of successful request served. 
        - Latency : measure percentile of request below thresholds.
        - Throughput : measure number of request successfully process in period of time.
        - Error rate: measure number of unsuccessful request
        - Business Specific metrics etc.
    ```

2. Define SLO
    ```text
        - System availability over certain period of time
        - Performance measurement with measurable metrics
        - Defining Error Budget and Acceptable downtime to release new features etc.
        - Business specific objective
    ```

3. Define SLA
    ```text
        - Defining agreement for penalties and incentives against SLO violation.
        - Defining terms and condition under which violation of SLO is legitimate.
        - Defining Incident Response management process
        - Communication and transparency in case of incident.
        - Establish Postmortems and RCA timelines etc.
    ```


#Actual Solution - Establishing SLA for payment orchestration platform

**Note: Values in the example are hypothetical ( do not consider them the real values )**

### Service :  Payment Request 

Step 1: Identity Key metrics
```text
        - Availability - Total number of successful / Total number of request * 100 
        - Error Rate 
        - Transaction Success Rate - number of successful transaction 
        - Orchestration Time - end to end time from payment initiation -> payment gateway -> psp acknowledgment -> user response
        - Latency for 90/95 percentile of request etc.
        - Concurrent Request Handling 	Metrics ( Perform Load Test with concurrent users, Benchmarking etc .)
        - Transaction Routing - routing request to the right psp etc.

```


Step 2: Define SLO 

| **SLO type** | **Objective** | 
| :---: | :---: |
|Availability |	98% |
|Latency	|90% of requests < 2 second
|Latency	|99% of requests < 3 second|
|Data Safety and Confidentially |	PCI DSS Compliance + Other Compliances as per financial regulations|
|Concurrent Request	|200 request per second|
|Throughput	|500 request per second|
|Transaction Success Rate|	99 %| 
|Error Rate 	|1%|
|Orchestration Time	|2 sec| 
|Notification Time |5 sec| 

		
Step 3: Define SLA ( defined based on SLO )
```text
        - Service will have uptime of 98% with right agreement of the penalties and incentives in case of failure to meet SLA.
        - Service will have response time of less than 2 second for 90 percentile of request and 3 seconds for 99 percentile of requests.
        - Service will adhere to all the compliance necessary for the secure transactions on the platform.
        - Service will can process max 500 transaction per second.
        - Technical support and Other Support model.
        - Exclusion if any application. 
```

Step 4: Remediation and Intimation plan
```text
        - Monitoring and Alerting system
        - Observability Pipelines ( Structured Logging, Traces, Metrics) 
        - Postmortems and RCA methodologies.
        - Automated Run-books and Playbooks
        - Establish right communication channel to quickly resolve the issue
        - Self healable infrastructure in place like simple/cross zone load balancing, autoscaling etc.
```

### Service : Payment History 		   	

Step 1: Identity Key metrics:

```text
        -  Availability 
        -  Error rate
        -  Latency 
        -  Requests frequency 
        -  Search speed
        -  History Retrieval Time
        -  Data accuracy / Completeness 
        -  Concurrency Handling
```
Step 2: define SLO  with examples 

Being an history service, we can keep SLO for this low, due to less critical in nature, Also we can save on cost by committing less throughput and 
reasonable latency on service response time.

| **SLO type** | **Objective** | 
| :---: | :---: |
|Availability |	95% |
|Latency	|90% of requests < 2 second
|Latency	|99% of requests < 3 second|
|Data Safety and Confidentially |	PCI DSS Compliance + Other Compliances as per financial regulations|
|Concurrent Request	|200 request per second|
|Throughput	|500 request per second|
|Transaction Success Rate|	99 %| 
|Error Rate 	|1%|
|Data Accuracy	|100%| 
	

Step 3:  SLA 
```text
        - Service will have uptime of 95% with right agreement of the penalties and incentives in case of failure to meet SLA.
        - Service will have response time of less than 2 second for 90 percentile of request and 3 seconds for 99 percentile of requests.
        - Service will adhere to all the compliance necessary for the secure transactions on the platform.
        - Service will can process max 500 transaction per second.
        - Technical support and Other Support
        - Exclusion if any 
```

### Service: payment gateway

Step 1: Identity Key metrics:
	
	Internal metrics
	
		- Availability - Total number of successful / Total number of request * 100 
		- Error Rate 
		- Latency for 90/95 percentile of request etc.		
		- Transaction Success Rate - number of successful transaction 
		- Transaction Process Time - time to complete the transaction with PSP ( like ) 
		- Notification Time 
		- Concurrent Request Handling 	Metrics ( Perform Load Test with concurrent users, Benchmarking etc .)
		- Timeout Errors - timeout due unavailability or late response from external system or psp
		

| **SLO type** | **Objective** | Outside Scope of our payment gateway
| :---: | :---: | :---: |
|Availability |	98% | | 
|Latency	|90% of requests < 2 second | Latency from PSP | 
|Latency	|99% of requests < 3 second| Latency from PSP | 
|Data Safety and Confidentially |	PCI DSS Compliance + Other Compliances as per financial regulations||
|Concurrent Request	|200 request per second| Limitation from PSP | 
|Throughput	|500 request per second| Limitation from PSP | 
|Transaction Success Rate|	99 %| |
|Error Rate 	|1%| | 
|Orchestration Time	|2 sec| | 
|Notification Time |5 sec| |


Step 3:  SLA
```text
        - Service will have uptime of 95% with right agreement of the penalties and incentives in case of failure to meet SLA.
        - Service will have response time of less than 2 second for 90 percentile of request and 3 seconds for 99 percentile of requests.
        - Service will adhere to all the compliance necessary for the secure transactions on the platform.
        - Service will can process max 500 transaction per second.
        - Service will not be considered failure if the downstream psp failed to successfully complete transaction.
        - Service will not be considered less responsive if the downstream latency increase in processing transaction.
        - Service will return appropriate response to the user in case on unavailability of downstream psp.
        - Technical support and Other Support
        - Exclusion if any 
```




