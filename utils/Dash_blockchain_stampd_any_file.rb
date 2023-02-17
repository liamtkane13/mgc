#!/usr/bin/env ruby

# Dash_blockchain_stampd_any_file.rb

%w[micro-optparse uri rubygems net/http pp aws-sdk awesome_print open3 mail fileutils].each {|z| require z} 

# Defines necessary command line args

opt = Parser.new do |p|
  p.banner = "Dash blockchain with stampd API"
  p.option :request, "the request to stampd, get or post", default:"post"
  p.option :file, "the file to blockchain", default:""
  end
options= opt.process!

if options[:file].empty?             
  STDERR.puts "I need an file"
  STDERR.puts opt.process!(['--help'])
  exit
end


# Credentials to sign into API

client_id = 'sv2-biao-liuECU'
secret_key = 'II6iklgC9T8sKQ1K'
blockchain = 'DASH'


# Creates the Hash for posting

aa=`shasum -a 256 #{options[:file]}`
hash=aa.split[0]
filename=aa.split[1].split("\/").last


# Signs into API

api_url_base = 'https://stampd.io/api/v2/hash'

uri = URI.parse(api_url_base)
args = {requestedURL: '/init', client_id: client_id, secret_key: secret_key}
uri.query = URI.encode_www_form(args)
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = api_url_base.match(/^https/)

login_request = Net::HTTP::Get.new(uri.request_uri)

login_response = http.request(login_request)
login_json = JSON.parse(login_response.body)
STDERR.puts login_json

if login_json.key?('code') && login_json['code'] == 300
  STDERR.puts 'Logged in successfully'
else
  STDERR.puts 'Login failed, exiting'
  abort
end


# Generates blockchain stamp

if options[:request]=="post"

uri = URI.parse(api_url_base)
args = {requestedURL: '/hash',
        sess_id: login_json['session_id'],
        hash: hash,
        blockchain: blockchain,
        meta_filename: filename,
}
uri.query = URI.encode_www_form(args)
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = api_url_base.match(/^https/)
post_request = Net::HTTP::Post.new(uri.request_uri)
post_response = http.request(post_request)
post_json = JSON.parse(post_response.body)
STDERR.puts post_json

record={'filename'=>filename, 'digest' => hash, 'txid' => post_json["txid"], 'url' => post_json["url"]}

