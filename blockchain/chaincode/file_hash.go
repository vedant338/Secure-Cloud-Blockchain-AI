package main

import (
	"encoding/json"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

type FileRecord struct {
	FileID    string `json:"file_id"`
	Hash      string `json:"hash"`
	Owner     string `json:"owner"`
	Timestamp string `json:"timestamp"`
}

func (s *SmartContract) AddFileHash(
	ctx contractapi.TransactionContextInterface,
	fileID string,
	hash string,
	owner string,
) error {

	record := FileRecord{
		FileID:    fileID,
		Hash:      hash,
		Owner:     owner,
		Timestamp: time.Now().UTC().String(),
	}

	data, _ := json.Marshal(record)
	return ctx.GetStub().PutState(fileID, data)
}

func (s *SmartContract) GetFileHash(
	ctx contractapi.TransactionContextInterface,
	fileID string,
) (*FileRecord, error) {

	data, err := ctx.GetStub().GetState(fileID)
	if err != nil || data == nil {
		return nil, err
	}

	var record FileRecord
	_ = json.Unmarshal(data, &record)
	return &record, nil
}

func main() {
	chaincode, _ := contractapi.NewChaincode(&SmartContract{})
	chaincode.Start()
}