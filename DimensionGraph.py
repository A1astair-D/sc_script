import networkx as nx
import os
import json
import sys
from collections import defaultdict, deque

new_limit = 2000
sys.setrecursionlimit(new_limit)

def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string

def remove_suffix(string, suffix):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string

def clean_underscores(string):
    return string.strip('_')

def process_jsonl_file(file_path):
    blacklisted_functions = [
        '$oltp-0.1.0.0-inplace$Product.OLTP.Transaction$proxyToCall',
    ]
    functions = []
    with open(file_path, 'r') as file:
        for line in file:
            func = json.loads(line)
            if func["coreName"] not in blacklisted_functions:
                functions.append(func)
    return functions

def build_unidirectional_dependency_graph(functions):
    G = nx.DiGraph()  # Directed graph
    for func in functions:
        core_name = func["coreName"]
        G.add_node(core_name)
        for var in func["vars"]:
            if var in G.nodes:
                G.add_edge(var, core_name)
    print(f"Global graph built with {len(G.nodes)} nodes and {len(G.edges)} edges.")
    return G

def traverse_directories_and_build_graph(root_dirs):
    all_functions = []
    for root_dir in root_dirs:
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".jsonL"):
                    file_path = os.path.join(subdir, file)
                    functions = process_jsonl_file(file_path)
                    all_functions.extend(functions)
    G = build_unidirectional_dependency_graph(all_functions)
    for func in all_functions:
        G.nodes[func["coreName"]]['data'] = func
    return G

def find_functions_for_service_conf(G, service_conf):
    function_list = []
    for func in G.nodes:
        lits = G.nodes[func].get('data', {}).get('lits', [])
        if service_conf in lits:
            if func not in function_list:
                function_list.append(func)
    return function_list

def search_and_aggregate_dimensions(G, function_list, dimensions_dict):
    SC_Results = defaultdict(list)
    for func in function_list:
        if func in G:
            result = bfs_search(G, func, dimensions_dict, False)
            for key, values in result.items():
                SC_Results[key].extend(values)
    for key in SC_Results:
        SC_Results[key] = list(set(SC_Results[key]))
    return SC_Results

def remove_blacklisted_items(current_func_dimensions):
    blacklisted_output = defaultdict(list)
    blacklisted_output["payment_instrument_group"] = ['REWARD']
    for key, values in blacklisted_output.items():
        if (key in current_func_dimensions) and (current_func_dimensions[key] == values):
            del current_func_dimensions[key]

def bfs_search(graph, start_node, dimensions_dict, reverse):
    queue = deque([start_node])
    visited = set()
    dimensions_result = defaultdict(list)
    while queue:
        current_node = queue.popleft()
        if current_node in visited:
            continue
        # print(f"Current function is {current_node}")
        visited.add(current_node)
        func_data = graph.nodes[current_node].get('data', {})
        current_func_dimensions = defaultdict(list)
        for key, values in dimensions_dict.items():
            for lit in func_data.get('lits', []):
                if lit in values and lit not in current_func_dimensions[key]:
                    current_func_dimensions[key].append(lit)
                    # print(f"lit found is {lit}")
            for var in func_data.get('vars', []):
                lit = var.split('$')[-1]
                if lit in values and lit not in current_func_dimensions[key]:
                    current_func_dimensions[key].append(lit)
                    # print(f"Var found is {lit}")
        remove_blacklisted_items(current_func_dimensions)
        add_current_to_main_dimensions(current_func_dimensions, dimensions_result)
        if reverse:
            for neighbor in graph.predecessors(current_node):
                if neighbor not in visited:
                    queue.append(neighbor)
        else:
            for neighbor in graph.successors(current_node):
                if neighbor not in visited:
                    queue.append(neighbor)
    return dimensions_result

def add_current_to_main_dimensions(current_func_dimensions, dimensions_result):
    for key, values in current_func_dimensions.items():
        if key not in dimensions_result:
            dimensions_result[key] = []
        for value in values:
            if value not in dimensions_result[key]:
                dimensions_result[key].append(value)

def update_payment_instrument_group_in_results(result_list):
    for result_item in result_list:
        if "dimensions_affected" in result_item:
            result = result_item["dimensions_affected"]
            if "payment_instrument_group" in result:
                if "CARD" in result["payment_instrument_group"]:
                    if "CREDIT CARD" not in result["payment_instrument_group"]:
                        result["payment_instrument_group"].append("CREDIT CARD")
                    if "DEBIT CARD" not in result["payment_instrument_group"]:
                        result["payment_instrument_group"].append("DEBIT CARD")
    return result_list

def find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions):
    cleaned_string = clean_underscores(remaining_string)
    broken_string = cleaned_string.split('_')
    dimensions_in_string = {}
    found_in_word_dict = {
        "AMEX": {"payment_instrument_group": ['CARD', 'CREDIT CARD', 'DEBIT CARD']},
        "DINERS": {"payment_instrument_group": ['CARD', 'CREDIT CARD', 'DEBIT CARD']},
        "MASTERCARD": {"payment_instrument_group": ['CARD', 'CREDIT CARD', 'DEBIT CARD']},
        "VISA": {"payment_instrument_group": ['CARD', 'CREDIT CARD', 'DEBIT CARD']},
        "RUPAY": {"payment_instrument_group": ['CARD', 'CREDIT CARD', 'DEBIT CARD']}
    }
    found_words = []
    #check for each substring
    for j in range(len(broken_string), 0, -1):
        for i in range(0, j):
            temp_string = '_'.join(broken_string[i:j])
            check_in_dimensions(dimensions_in_string, temp_string, dimensions)
            if temp_string in found_in_word_dict:
                found_words.append(temp_string)
    replace_extra_dimensions(dimensions_in_string)
    #add everything to result
    for dim_key, dim_value in dimensions_in_string.items():
        dimensions_results[dim_key] = dim_value
    #replace if found from string
    for found_word in found_words:
        replacement_dict = found_in_word_dict[found_word]
        for key, replacement_value in replacement_dict.items():
            dimensions_results[key] = replacement_value

def check_in_dimensions(dimensions_results, cleaned_string, dimensions):
    for dimension, values in dimensions.items():
        if cleaned_string in values:
            if dimension not in dimensions_results:
                dimensions_results[dimension] = []
            if cleaned_string not in dimensions_results[dimension]:
                dimensions_results[dimension].append(cleaned_string)
            return True
    return False

def replace_extra_dimensions(result):
    extraDict = {
        "NB": {"payment_instrument_group": ['NET BANKING']},
        "NET_BANKING": {"payment_instrument_group": ['NET BANKING']},
        "DEBIT_CARD": {"payment_instrument_group": ['DEBIT CARD']},
        "CREDIT_CARD": {"payment_instrument_group": ['CREDIT CARD']},
        "CARDS": {"payment_instrument_group": ['CARD']},
        "CVVLESS": {"payment_instrument_group": ['CARD']},
    }
    if 'extra' in result:
        extra_values = result.pop('extra', [])
        for extra_value in extra_values:
            if extra_value in extraDict:
                for dim_key, dim_values in extraDict[extra_value].items():
                    if dim_key not in result:
                        result[dim_key] = []
                    for dim_val in dim_values:
                        if dim_val not in result[dim_key]:
                            result[dim_key].append(dim_val)

def add_to_results_list(results_list, original_str, temp_str, dimensions_results):
    for key in dimensions_results:
        dimensions_results[key] = sorted(dimensions_results[key])
    result_obj = {
        "input_service_config" : original_str,
        "lit_found_in_code"    : temp_str,
        "dimensions_affected"  : dimensions_results
    }
    results_list.append(result_obj)

def handle_no_match_case(original_str, dimensions, results_list):
    dimensions_results = {}
    words = original_str.split('_')
    #check first 4 words
    for i in range(1, min(5, len(words) + 1)):
        remaining_string = '_'.join(words[:i])
        remaining_string = remaining_string.upper()
        find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions)
    #check last 4 words
    for i in range(1, min(5, len(words) + 1)):
        remaining_string = '_'.join(words[-i:])
        remaining_string = remaining_string.upper()
        find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions)
    #add to result
    add_to_results_list(results_list, original_str, "", dimensions_results)

def save_to_json(sc_result, output_file):
    with open(output_file, 'w') as file:
        json.dump(sc_result, file, indent=4)

def remove_items_from_payment_gateway(dimensions, items_to_remove):
    payment_gateway_list = dimensions.get("payment_gateway", [])
    dimensions["payment_gateway"] = [item for item in payment_gateway_list if item not in items_to_remove]
    return dimensions

def remove_items_from_payment_instrument_group(dimensions, items_to_remove):
    payment_gateway_list = dimensions.get("payment_instrument_group", [])
    dimensions["payment_instrument_group"] = [item for item in payment_gateway_list if item not in items_to_remove]
    return dimensions

def remove_key_if_exceeds_threshhold(key, threshold, result):
    if "dimensions_affected" in result:
        result_da = result["dimensions_affected"]
        if key in result_da:
            if len(result_da[key]) >= threshold:
                del result_da[key]
    return

def getDimensionsAffectedForSCs(input_file, output_file):
    given_dimensions = {
        # "txn_type": ['AUTH_AND_SETTLE', 'AUTH_AND_SPLIT_SETTLE', 'PREAUTH_AND_SETTLE', 'ZERO_AUTH'],
        # "txn_object_type": ['EMANDATE_PAYMENT', 'EMANDATE_REGISTER', 'MANDATE_PAYMENT', 'MANDATE_REGISTER', 'ORDER_PAYMENT', 'PARTIAL_CAPTURE', 'TPV_EMANDATE_PAYMENT', 'TPV_EMANDATE_REGISTER', 'TPV_PAYMENT', 'VAN_PAYMENT'],
        # "source_object": ['AUTH_PROVIDER_FALLBACK_TO_THREE_DS', 'CRED_COLLECT', 'CRED_INTENT', 'CUSTOMER_FALLBACK_TO_THREE_DS', 'DECIDER_FALLBACK_TO_THREE_DS', 'DIRECT_WALLET_DEBIT', 'DIRECT_WALLET_LINK_AND_DEBIT', 'MANDATE', 'MERCHANT_FALLBACK_TO_THREE_DS', 'PAYMENT_CHANNEL_FALLBACK_TO_THREE_DS', 'PG_FAILURE_FALLBACK_TO_THREE_DS', 'PUSH_PAY', 'REDIRECT_WALLET_DEBIT', 'TOKENIZATION_CONSENT_FALLBACK_TO_THREE_DS', 'TXN_SUB_DETAIL', 'UPI_COLLECT', 'UPI_INAPP', 'UPI_PAY', 'UPI_QR', 'VAN_NB'],
        "payment_gateway": ['ADYEN', 'AIRPAY', 'AIRTELMONEY', 'AMAZONPAY', 'AMEX', 'ATOM', 'AXIS_BIZ', 'AXIS_UPI', 'BAJAJFINSERV', 'BHARATX', 'BILLDESK', 'BOKU', 'CAMSPAY', 'CAPITALFLOAT', 'CAREEMPAY', 'CASH', 'CCAVENUE_V2', 'CHECKOUT', 'CRED', 'CYBERSOURCE', 'DIGIO', 'DUMMY', 'EASEBUZZ', 'EBS_V3', 'EPAYLATER', 'FAWRYPAY', 'FREECHARGE', 'GOCASHFREE', 'GOOGLEPAY', 'HDFC', 'HDFC_CC_EMI', 'HDFC_UPI', 'HSBC', 'HSBC_UPI', 'HYPERPAY', 'HYPERPG', 'HYPER_PG', 'IATAPAY', 'ICICI_UPI', 'INDUS_PAYU', 'IPG', 'ITZCASH', 'JIOMONEY', 'LAZYPAY', 'LOANTAP', 'LOTUSPAY', 'LSP', 'MERCHANT_CONTAINER', 'MIGS', 'MOBIKWIK', 'MOBIKWIKZIP', 'MORPHEUS', 'MPGS', 'NAVITAIRE', 'NOON', 'OLAPOSTPAID', 'PAYFORT', 'PAYGLOCAL', 'PAYPAL', 'PAYTM', 'PAYTM_V2', 'PAYU', 'PAYZAPP', 'PHONEPE', 'PINELABS', 'QWIKCILVER', 'RAZORPAY', 'RBL_BIZ', 'SBI', 'SHOPSE', 'SIKA_SIMPL', 'SIMPL', 'SNAPMINT', 'SODEXO', 'STRIPE', 'TAP', 'TATAPAY', 'TATAPAYLATER', 'TATA_PA', 'TPSL', 'TWID', 'TWID_V2', 'TWOC_TWOP', 'WORLDPAY', 'YESBANK_UPI', 'YES_BIZ', 'ZAAKPAY'],
        "payment_instrument_group": ['AADHAAR', 'CARD', 'CASH', 'CONSUMER_FINANCE', 'CREDIT CARD', 'DEBIT CARD', 'MERCHANT_CONTAINER', 'NET BANKING', 'REWARD', 'RTP', 'UPI', 'VIRTUAL_ACCOUNT', 'WALLET'],
        # "auth_type": ['FIDO', 'MOTO', 'NO_THREE_DS', 'OTP', 'THREE_DS', 'THREE_DS_2', 'TWO_DS'],
        # "action": ['INCOMING_API', 'OUTGOING_API'],
        # "payment_flow": ["AUTO_DISBURSEMENT", "AUTO_USER_REGISTRATION", "BANK_INSTANT_REFUND", "MANDATE_PREDEBIT_NOTIFICATION_DISABLEMENT", "ORDER_AMOUNT_AS_SUBVENTION_AMOUNT", "ORDER_ID_AS_RECON_ID", "PASS_USER_TOKEN_TO_GATEWAY", "S2S_FLOW", "SPLIT_SETTLE_ONLY", "SUBSCRIPTION_ONLY", "TOPUP", "TPV_ONLY", "TXN_UUID_AS_TR", "UPI_INTENT_REGISTRATION", "V2_INTEGRATION", "V2_LINK_AND_PAY", "VPOS2", "WALLET_COLLECT", "WALLET_INTENT", "ADDRESS_VERIFICATION", "ALTID", "AUTHN_AUTHZ", "AUTHZ_CAPTURE", "AUTO_REFUND", "CAPTCHA", "DYNAMIC_CURRENCY_CONVERSION", "ELIMINATION_BASED_ROUTING", "INSTANT_REFUND", "MANDATE_WORKFLOW", "OFFER", "OUTAGE", "PART_PAYMENT", "PAYMENT_COLLECTION_LINK", "PAYMENT_FORM", "PAYMENT_LINK", "RISK_CHECK", "SI_HUB", "SPLIT_PAYMENT", "SR_BASED_ROUTING", "STANDALONE_AUTHENTICATION", "STANDALONE_AUTHORIZATION", "STANDALONE_CAPTURE", "SURCHARGE", "TA_FILE", "CARD_DOTP", "CARD_MOTO", "CARD_NO_3DS", "CARD_VIES", "CARD_ZERO_AUTH", "CVVLESS", "DIRECT_DEBIT", "DOTP", "EMANDATE", "EMI", "MANDATE", "PARTIAL_CAPTURE", "PREAUTH", "SDKLESS_INTENT", "SPLIT_SETTLE", "SPLIT_SETTLEMENT", "TPV", "VISA_CHECKOUT", "ZERO_AUTH", "CARD_3DS2", "CARD_TOKENIZATION", "FIDO", "ASYNC", "CARD_3DS", "COLLECT", "DIRECT_BANK_EMI", "EMANDATE_PAYMENT", "EMANDATE_REGISTER", "INAPP", "INAPP_DEBIT", "INTENT", "INTERNAL_LOW_COST_EMI", "INTERNAL_LOW_COST_EMI_SPLIT", "INTERNAL_NO_COST_EMI", "INTERNAL_NO_COST_EMI_SPLIT", "ISSUER_TOKEN_CREATED", "ISSUER_TOKEN_USED", "LINK_AND_DEBIT", "LOCKER_TOKEN_CREATED", "LOCKER_TOKEN_USED", "LOW_COST_EMI", "MANDATE_PAYMENT", "MANDATE_REGISTER", "MANDATE_REGISTER_DEBIT", "NETWORK_TOKEN_CREATED", "NETWORK_TOKEN_USED", "NEW_CARD", "NO_COST_EMI", "OFFLINE", "PAYU_TOKEN_USED", "PUSH_PAY", "QR", "REDIRECT_DEBIT", "SODEXO_TOKEN_CREATED", "SODEXO_TOKEN_USED", "STANDARD_EMI", "STANDARD_EMI_SPLIT"],
        "extra": ['NB', 'NET_BANKING', 'DEBIT_CARD', 'CREDIT_CARD', 'CARDS', 'CVVLESS']
    }

    items_to_remove = ["CASH", "AMEX"]
    dimensions = remove_items_from_payment_gateway(given_dimensions, items_to_remove)
    items_to_remove = ["REWARD"]
    dimensions = remove_items_from_payment_instrument_group(dimensions, items_to_remove)
    
    def read_input_file(file_path):
        with open(file_path, 'r') as file:
            input_lines = file.readlines()
        return [line.strip() for line in input_lines]

    test_list = read_input_file(input_file)

    euler_order_directory = "directories_data/euler_order_directory"
    euler_gateway_directory = "directories_data/euler_gateway_directory"
    euler_txns_directory = "directories_data/euler_txns_directory"
    euler_txns_euler_x_directory = "directories_data/euler_txns_euler_x_directory"
    euler_txns_oltp_directory = "directories_data/euler_txns_oltp_directory"
    euler_txns_euler_decider_directory = "directories_data/euler_txns_euler_decider_directory"
    euler_customer_directory = "directories_data/euler_customer_directory"
    euler_cards_directory = "directories_data/euler_cards_directory"
    euler_pre_txn_directory = "directories_data/euler_pre_txn_directory"
    euler_pre_txn_apiTypes_directory = "directories_data/euler_pre_txn_apiTypes_directory"
    root_directories = [euler_gateway_directory, euler_order_directory, euler_customer_directory, euler_pre_txn_directory, euler_pre_txn_apiTypes_directory, euler_cards_directory, euler_txns_directory, euler_txns_euler_x_directory, euler_txns_oltp_directory, euler_txns_euler_decider_directory]

    # Build the graph
    G = traverse_directories_and_build_graph(root_directories)
    results_list = []

    for i, original_str in enumerate(test_list):
        print(f"Running with service_configuration : {original_str}")
        temp_str = original_str
        found = False
        for _ in range(7):
            if '_' in temp_str:
                function_list = find_functions_for_service_conf(G, temp_str)
                if function_list:
                    dimensions_results = search_and_aggregate_dimensions(G, function_list, dimensions)
                    dimensions_results = {}
                    replace_extra_dimensions(dimensions_results)
                    remaining_string = remove_prefix(original_str, temp_str)
                    find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions)
                    add_to_results_list(results_list, original_str, temp_str, dimensions_results)
                    found = True
                    break

                # Modify temp_str for the next iteration
                if temp_str[-1] == '_':
                    temp_str = temp_str[:-1]
                else:
                    temp_str = temp_str.rsplit('_', 1)[0]
                    if '_' in temp_str :
                        temp_str = temp_str + '_'
                    else :
                        break
            else:
                break
        
        if found:
            continue
        temp_str = original_str
        for _ in range(7):
            if '_' in temp_str:
                function_list = find_functions_for_service_conf(G, temp_str)
                if function_list:
                    dimensions_results = search_and_aggregate_dimensions(G, function_list, dimensions)
                    dimensions_results = {}
                    replace_extra_dimensions(dimensions_results)
                    remaining_string = remove_suffix(original_str, temp_str)
                    find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions)
                    add_to_results_list(results_list, original_str, temp_str, dimensions_results)
                    found = True
                    break

                # Modify temp_str for the next iteration
                if temp_str[0] == '_':
                    temp_str = temp_str[1:]
                else:
                    temp_str = temp_str.split('_', 1)[1] 
                    if '_' in temp_str :
                        temp_str = '_' + temp_str
                    else :
                        break
            else:
                break

        if not found:
            handle_no_match_case(original_str, dimensions, results_list)
        
    print(f"Adding related dimensions for CARD")
    update_payment_instrument_group_in_results(results_list)
    print(f"Removing key if exceeds threshold")
    for result in results_list:
        remove_key_if_exceeds_threshhold("payment_gateway", 5, result)
        remove_key_if_exceeds_threshhold("payment_instrument_group", 5, result)

    output_dir = "results_directory"
    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, output_file)
    save_to_json(results_list, output_file_path)
    print(f"SC_Results have been saved to {output_file_path}")


input_file = "service_configurations.txt"
# input_file = "problem_input.txt"
input_file = "test_input.txt"
output_file = "Dimensions_affected_only_word.json"
# output_file = "problem_output.json"
output_file = "test_output.json"
callFunc = getDimensionsAffectedForSCs(input_file, output_file)