{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE OverloadedStrings #-}

import Control.Monad (forM_)
import Data.Aeson (FromJSON, ToJSON, decode, encode, withObject, (.:), (.=), Value, object)
import Data.ByteString.Lazy (ByteString, readFile, writeFile)
import Data.List (nub, intercalate)
import Data.Map (Map)
import qualified Data.Map as Map
import GHC.Generics (Generic)
import System.Directory (createDirectoryIfMissing)
import System.FilePath ((</>))

-- Data structure for Row
data Row = Row
    { configName :: String
    , newValue :: String
    , currentValue :: String
    } deriving (Generic)

instance FromJSON Row where
    parseJSON = withObject "Row" $ \v -> Row
        <$> v .: "configName"
        <*> v .: "newValue"
        <*> v .: "currentValue"

instance ToJSON Row where
    toJSON (Row name new current) = object
        ["configName" .= name, "newValue" .= new, "currentValue" .= current]

-- Function to clean underscores from a string
cleanUnderscores :: String -> String
cleanUnderscores = trim . stripPrefix "_" . stripSuffix "_" where
    trim = dropWhile (== ' ')
    stripPrefix p xs = if take (length p) xs == p then drop (length p) xs else xs
    stripSuffix s xs = if reverse (take (length s) (reverse xs)) == s then take (length xs - length s) xs else xs

-- Combine dimensions from two results
combineDimensionsAffectedResult :: Map String [String] -> Map String [String] -> Map String [String]
combineDimensionsAffectedResult dims1 dims2 = Map.map mergeDimensions commonKeys
  where
    commonKeys = Map.keys dims1 `intersect` Map.keys dims2
    mergeDimensions key = nub (dims1 Map.! key ++ (dims2 Map.! key))

-- Save JSON to file
saveToJson :: FilePath -> Value -> IO ()
saveToJson path value = writeFile path (encode value)

-- Load JSON from file
loadJsonFromFile :: FilePath -> IO (Maybe [Row])
loadJsonFromFile filePath = do
    jsonData <- readFile filePath
    return $ decode jsonData

-- Create dimensions map
makeDimensionsArray :: Map String [String]
makeDimensionsArray = Map.fromList
    [ ("merchant_id", ["com.swiggy", "swiggy-nf", "licious", "moneyview", "tatapay"])
    , ("payment_gateway", ["ADYEN", "AIRPAY", "AIRTELMONEY", "AMAZONPAY", "AMEX"])
    , ("payment_instrument_group", ["AADHAAR", "CARD", "CASH", "CREDIT CARD", "DEBIT CARD"])
    , ("extra", ["NB"])
    ]

-- Extract strings from a JSON object
extractStrings :: Value -> [String]
extractStrings (Object o) = concatMap extractStrings (Map.elems o)
extractStrings (Array a)  = concatMap extractStrings (V.toList a)
extractStrings (String s)  = [s]
extractStrings _           = []

-- Function to find dimensions in strings
checkInDimensions :: Map String [String] -> String -> Map String [String] -> Map String [String]
checkInDimensions results cleanedString dimensions =
    foldl addDimension results (Map.toList dimensions)
  where
    addDimension acc (dimKey, dimValues) =
        if cleanedString `elem` dimValues
        then Map.insertWith (++) dimKey [cleanedString] acc
        else acc

-- Main function
main :: IO ()
main = do
    let filePath = "BSJson4.json"
    let outputDir = "results_directory2"
    let outputFile = "dimensions_affected.json"
    
    jsonData <- loadJsonFromFile filePath
    case jsonData of
        Nothing -> putStrLn "Failed to decode JSON."
        Just rows -> do
            createDirectoryIfMissing True outputDir
            let results = map processRow rows
            saveToJson (outputDir </> outputFile) (encode results)
            putStrLn $ "Results saved to " ++ (outputDir </> outputFile)

-- Process each row to extract dimensions
processRow :: Row -> Value
processRow row = 
    let dimAffectedNew = dimensionsAffectedObject (newValue row) dimensions
        dimAffectedCurrent = dimensionsAffectedObject (currentValue row) dimensions
        dimAffectedCombined = combineDimensionsAffectedResult dimAffectedNew dimAffectedCurrent
    in object ["configName" .= configName row, "dimensions_affected" .= dimAffectedCombined]

-- Function to handle dimensions affected by a given JSON string
dimensionsAffectedObject :: String -> Map String [String] -> Map String [String]
dimensionsAffectedObject jsonString dimensions =
    let jsonValue = decode jsonString
        stringListNewValue = extractStrings jsonValue
    in foldl (\acc val -> checkInDimensions acc val dimensions) Map.empty stringListNewValue

