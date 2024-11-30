import subprocess
import json

# execute_command
# args: 
#    'command'(str) command to be executed
# -----
# returns:
#    stdout
#    stderr
#    returncode  
def execute_command(command):
   try:
      # Run the command and capture its output and error
      result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
      # Print the standard output
      # print("Standard Output:")
      # print(result.stdout)
     
      # # Print the standard error
      # print("Standard Error:")
      # print(result.stderr)

      # # Print the return code
      # print("Return Code:", result.returncode)

   except subprocess.CalledProcessError as e:
      print("Command execution failed.")
      print("Return Code:", e.returncode)
      print("Error:", e.stderr)
      exit(8)

   if result.returncode!=0:
      print('rc', result.returncode)
      print('sto ', result.stdout)
      print('ste ', result.stderr)
      exit(8)

   return result.stdout, result.stderr, result.returncode  


# check_zos_file
# args: 
#    'file'(str) file name to check
# -----
# returns:
#    True or False
def check_zos_file(file):
   file=file.upper()
   command=f'zowe zos-files list data-set "{file}"'
   # print(command)
   print(f'Checking {file} ...')
   sto, ste, rc = execute_command(command)
   if file in sto: return(True)
   else: return(False)


# del_zos_file
# args: 
#    'file'(str) file to be deleted
# -----
# returns:
def del_zos_file(file):
   command=f'zowe zos-files delete data-set "{file}" -f'
   # print(command)
   print(f'Deleting {file} ...')
   sto, ste, rc = execute_command(command)


# cre_trs_file
# args: 
#    'file'(str) file name
# -----
# returns:
def cre_trs_file(file):
   command=f'zowe zos-files create ps "{file}" --rl 1024 --bs 1024 --rf FB --sz 10CYL'
   # print(command)
   print(f'Creating {file} ...')
   sto, ste, rc = execute_command(command)


# upload_zos_file
# args: 
#    'remote_file'(str) zos file name
#    'local_file'(str) local file name - full path if not in same dir
#       sample local_file='.\\somedir\\temp.txt' 
#    'flags'(str) zowe flags '-b'
# -----
# returns:
def upload_zos_file(remote_file, local_file, flags=''):
   remote_file=remote_file.upper()
   command=f'zowe zos-files upload file-to-data-set "{local_file}" "{remote_file}" {flags}'
   # print(command)
   print(f'Uploading {local_file} to {remote_file} ...')
   sto, ste, rc = execute_command(command)


# download_zos_file
# args: 
#    'remote_file'(str) zos file name
#    'local_file'(str) local file name - full path if not in same dir
#       sample local_file='.\\somedir\\temp.txt' 
#    'flags'(str) zowe flags '-b'
# -----
# returns:
def download_zos_file(remote_file, local_file, flags=''):
   remote_file=remote_file.upper()
   command=f'zowe zos-files download data-set "{remote_file}" -f "{local_file}" {flags}'
   # print(command)
   print(f'Downloading in {local_file} ...')
   sto, ste, rc = execute_command(command)

# submit_local_jcl (wait for execution and response in json format)
# args: 
#    'jcl'(str) local file name - full path if not in same dir
#        sample: jcl='.\\jcl\\temp.jcl'   
#    'flags'(str) zowe flags '-d -e'
# -----
# returns:
#    ret_cod
#    jobid
def submit_local_jcl(jcl,flags=''):
   command=f'zowe zos-jobs submit local-file "{jcl}" {flags} --wfo --rfj'
   # print(command)
   print(f'Submiting {jcl} ...')
   sto, ste, rc = execute_command(command)
   sto = json.loads(sto)
   ret_cod=sto.get('data', {}).get('retcode')
   jobid=sto.get('data', {}).get('jobid')

   return(ret_cod,jobid)    


# find_userid
# args: 
# -----
# returns:
#   userid
def find_userid():
   command="zowe uss issue command 'who'"
   # print(command)
   print('Finding userid ...')
   sto, ste, rc = execute_command(command)
   userid = sto.split(" ")[1]
   return(userid)


# check_zos_file_name
# args: 
#    'file'(str) file name to check
# -----
# returns:
#    True - False 
#    message
def check_zos_file_name(file):
   file=file.upper()
   tf=True
   message='Correct File Name'
   if len(file)>44:
      tf=False
      message='Error: A data set name cannot be longer than 44 characters'
   elif '.' not in file:
      tf=False
      message='Error: A data set name must be composed of at least two joined character segments (qualifiers), separated by a period (.)'
   elif '..' in file:
      tf=False
      message='Error: A data set name cannot contain two successive periods'
   elif file[-1]=='.':
      tf=False
      message='Error: A data set name cannot end with a period'
   else:
      hlqs=file.split('.')
      valid_first_char=''.join(chr(i) for i in range(ord('A'), ord('Z') + 1))+'#@$'
      valid_rest =''.join(chr(i) for i in range(ord('0'), ord('9') + 1))+valid_first_char+'-'
      for hlq in hlqs:
         if len(hlq)>8:
            tf=False
            message='Error: A segment cannot be longer than eight characters'
         elif hlq[0] not in valid_first_char:
            tf=False
            message='Error: The first segment character must be either a letter or one of the following three special characters: #, @, $'
         else: 
            for i in hlq[1:]:
               if i not in valid_rest:
                  tf=False
                  message='Error: The remaining seven characters in a segment can be letters, numbers, special characters (only #, @, or $), or a hyphen (-)'

   return(tf,message)