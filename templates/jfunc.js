function save(){
    $('#save_feedback').html('your profile has been update!');
    $('#save_feedback').fadeIn(500);
    $('#save_feedback').delay(2000);
    $('#save_feedback').fadeOut(500);
}





if chosen_option >= 100:
                flow = model.session.query(model.Flow).filter_by(flow_id=chosen_option).all()
                for chosen_option in flow:
                    breaths += chosen_option.breaths 
                    trigram_chain.append((chosen_option.asana, chosen_option.breaths))
                new_key=(chosen_option[-2],chosen_option[-1])

            else:
                breaths += chosen_option.breaths 
                trigram_chain.append((chosen_option, chosen_option.breaths))
                new_key = (new_key[1],chosen_option)