
<template>
  <v-container>
    <v-layout text-xs-center wrap >

   	<v-flex xs12 >
		<v-alert 
			v-model="success"
			transition="scale-transition"
      			dismissible
      			type="success"
    			>
      			You reached the next level
    		</v-alert>
	 	<v-alert 
			v-model="false_answer"
			transition="scale-transition"
			dismissible
			type="error"
			>
			Wrong answer Loser!
		</v-alert>
		<v-progress-linear v-model="valueDeterminate"></v-progress-linear>
	</v-flex>
   </v-layout>	
   <v-layout text-xs-center wrap >

	<v-flex xs4 offset-xs2 >
		<fieldset>
			<input type="text" placeholder="Your answer" @focus="show" data-layout="compact" />
		</fieldset>
	</v-flex>
	<v-flex xs1 class="mt-4">
			<v-btn left  :disabled="disabled_solve" v-if="!visible" @click="solve_answer()" color="success">Solve riddle</v-btn>
	</v-flex>
   </v-layout>	
   <v-layout v-if="!visible" text-xs-center wrap>
	<v-flex>
		<v-btn  color="info" @click="lower_level()" :disabled="disabled_back">Back</v-btn>
	</v-flex> 
	<v-flex>
		<v-card>
			<v-card-text>Level {{current_question+1}}</v-card-text>
		</v-card>
	</v-flex>
	<v-flex >
		<v-btn  color="info" :disabled="disabled_next" @click="add_level()">Next</v-btn>
	</v-flex>
   </v-layout>	
   <v-layout text-xs-center wrap >
	<v-flex xs12 v-if="!visible">
		<v-btn @click="read_text()" color="info">Play Audio</v-btn>
		<v-btn @click="stop_audio()" color="error">Stop</v-btn>
	</v-flex>

	<v-flex xs12 v-if="!visible">
		<v-btn small color="warning" @click="reset()">Reset all levels</v-btn>
		<v-btn small @click="shutdown()" color="error">Shutdown</v-btn>
		<v-btn small  @click="reboot()" color="error">Reboot</v-btn>
	</v-flex>

	<v-flex xs12>
		<vue-touch-keyboard 
			:options="options" 
			v-if="visible" 
			:layout="layout" 
			:cancel="accept" 
			:accept="accept" 
			:input="input" />

	</v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {

	data: () => ({
		max_questions:6,
		current_question:0,
		current_level:0,
		valueDeterminate:0,
		visible: false,
		disabled_solve: false,
		disabled_next: false,
		disabled_back: false,
	      	layout: "normal",
	      	input: null,
		success: false,
		false_answer: false,
	      	options: {
			useKbEvents: false,
			preventClickEvent: false}
	}),
	
	created: function(){
		this.current_question=0
		this.reload_state()
		this.set_state()
	},

	watch: {
    		current_question: function () {
			this.recalc_status()
			console.log("log")
			this.set_state()
		},
		current_level:function(){
			this.current_question=this.current_level
			this.read_text()
			this.set_state()
		}


	},
	
	methods: {


		accept(text) {
			this.input=text;
			this.hide();
		},
		
		set_state(){
			console.log("state")
			if (this.current_question<this.current_level){
				this.disabled_solve=true
				this.disabled_next=false
			}
			else{
				console.log("hit")
				this.disabled_solve=false
				this.disabled_next=true
			}
			if(this.current_level==this.max_questions)
			{
				console.log("hitti")
				this.disabled_solve=true
			}
			
			if(this.current_question==0)
			{
				this.disabled_back=true
			}
			else
			{
				this.disabled_back=false
			}
		},
		

		show(e) {
			this.input = e.target;
			this.layout = e.target.dataset.layout;

			if (!this.visible)
				this.visible = true
		},


		hide() {
			this.visible = false;
		},


		reset(){
			this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/reset")
				.then(response => (
					this.reload_state()
					)
				)
		},

		shutdown(){
			this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/shutdown")
				.then(response => (
					this.update_state(response)
					)
				)
		},
	

		reboot(){
			this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/reboot")
				.then(response => (this.update_state(response))
				)
		},


		reload_state:function(){
			this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/state")
				.then(response => (this.update_state(response)))
		},

		update_state:function(response){
			console.log(response)
			this.max_questions = response.data.num_levels-1
			this.current_level = response.data.max_level
			this.current_question = this.current_level
		},
	
		solve_answer:function(){
			console.log(window.location.hostname);
			var url = "http://"+window.location.hostname+":"+window.location.port+"/api/solve/"+this.current_question+"/"+this.input 
			this.axios.get(url)
				.then(response =>{ 
					this.reload_state();
					if(response.status==202){
						this.success=true;
						this.input=""
					};
					if(response.status==204){
						this.false_answer=true;
					}
				})
		},


		read_text:function(){
			this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/level/"+this.current_question)
		},


		stop_audio:function(){
			this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/stop");
		},


		delete_number: function(){
			this.answer=[]
		},


		recalc_status: function(){
			this.valueDeterminate = 100/this.max_questions * this.current_question
		},


		add_level:function(){
			this.change_current(1)
		},
		

		lower_level:function(){
			this.change_current(-1)
		},


		change_current:function(changed){
			if(this.current_question+changed<=this.max_questions && this.current_question+changed>=0)
			{
				if(this.current_level >= this.current_question + changed){
					this.current_question+=changed;
				}
			}
		}
	}
  }
</script>

<style>
html {
	font-family: Tahoma;
	font-size: 12px;
}

#keyboard {
	position: fixed;
	left: 0;
	right: 0;
	bottom: 0;

	z-index: 1000;
	width: 100%;
	max-width: 1000px;
	margin: 0 auto;

	padding: 1em;

	background-color: #EEE;
	box-shadow: 0px -3px 10px rgba(black, 0.3);

	border-radius: 10px;
}

fieldset {
	display: block;
	/*width: 200px;*/
	padding: 15px;
	margin: 15px auto;
	border-style: solid;
	background-color: #fff;
	border-color: #ddd;
	border-width: 1px;
	border-radius: 4px;	
}

input {
	display: block;
	width: 100%;
	height: 34px;
	padding: 6px 12px;
	font-size: 14px;
	line-height: 1.42857143;
	color: #555;
	background-color: #fff;
	background-image: none;
	border: 1px solid #ccc;
	border-radius: 4px;
	box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
	transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;		

	&:focus {
		border-color: #66afe9;
		outline: 0;
		box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6);			
	}
}
</style>
