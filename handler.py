"""
AWS Lambda handler for DNA BLAST application.
"""
import json
import os
from app import validate_fasta, perform_blast, parse_blast_results

def blast(event, context):
    """
    Lambda handler for BLAST endpoint.
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        body = json.loads(event.get('body', '{}'))
        fasta_text = body.get('fasta_text', '')

        if not fasta_text:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'No FASTA sequence provided'
                })
            }

        is_valid, result = validate_fasta(fasta_text)
        if not is_valid:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': result
                })
            }

        sequences = result
        if not sequences:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'No valid sequences found'
                })
            }

        sequence = sequences[0]
        blast_record = perform_blast(sequence)

        if blast_record is None:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'BLAST search failed. Please try again.'
                })
            }

        hits = parse_blast_results(blast_record)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'query_id': sequence.id,
                'query_length': len(sequence.seq),
                'hits': hits
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }

def serve_frontend(event, context):
    """
    Lambda handler to serve the frontend HTML.
    """
    headers = {
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
    }

    try:
        with open('templates/index.html', 'r') as f:
            html_content = f.read()

        return {
            'statusCode': 200,
            'headers': headers,
            'body': html_content
        }
    except FileNotFoundError:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Frontend not found'})
        }