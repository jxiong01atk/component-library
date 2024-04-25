from sqlalchemy import create_engine, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from db_alchemy_model import Idea, Part, PartCosts, PartHasIdea, PartInProduct, Product, Spendcube
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from constants import dbstring

Base = declarative_base()

def get_spend_cube_records():
    # Create the database engine
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)  # Ensure all tables are created based on Base's current state
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
        Spendcube.id,
        Spendcube.buyer,
        Spendcube.actual_pay_date,
        Spendcube.invoice_number,
        Spendcube.po_number,
        Spendcube.po_line,
        Spendcube.segment,
        Spendcube.sector,
        Spendcube.division,
        Spendcube.site_location,
        Spendcube.unit,
        Spendcube.subunit,
        Spendcube.program_area,
        Spendcube.business_area,
        Spendcube.project,
        Spendcube.company_code,
        Spendcube.data_source,
        Spendcube.supplier_name,
        Spendcube.erp_supplier_id,
        Spendcube.std_supplier_id,
        Spendcube.mdg_id,
        Spendcube.physical_city,
        Spendcube.physical_state,
        Spendcube.physical_country,
        Spendcube.physical_address,
        Spendcube.naics,
        Spendcube.category_team,
        Spendcube.supplier_level_1,
        Spendcube.supplier_level_2,
        Spendcube.supplier_level_3,
        Spendcube.pt_group_value,
        Spendcube.pay_terms,
        Spendcube.order_date_inv,
        Spendcube.invoice_date,
        Spendcube.invoice_description,
        Spendcube.part,
        Spendcube.part_description,
        Spendcube.mfr_part,
        Spendcube.commodity_desc_po,
        Spendcube.commodity_code_po,
        Spendcube.quantity,
        Spendcube.spend,
        Spendcube.mpn,
        Spendcube.price,
        # Spendcube.in_scope_part_id,
        # Spendcube.part_rationale,
        # Spendcube.data_quality,
        Spendcube.segment_reclassify,
        Spendcube.sector_reclassify,
        Spendcube.category_team_remapping,
        # Spendcube.forecast_description,
        Spendcube.supplier_name_standardized,
        Spendcube.supplier_in_wave_1
    )

    # Execute the query and fetch all records
    results = query.all()
    session.close()
    return results
# Populate with current csv
def get_idea_desc_list():
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
        Idea.id,
        Idea.source, 
        Idea.type, 
        Idea.description, 
    )

    results = query.all()
    session.close()
    
    return results

def get_ideas():
    engine = create_engine(dbstring, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
        Part.id,
        Part.part_number, 
        Part.description, 
        Idea.id,
        Idea.source, 
        Idea.type, 
        Idea.description, 
        Idea.alternate_pn,
        Idea.status,
        Idea.il,
        Idea.notes,    
        Idea.baseline_cost_source,  
        PartCosts.cost,
        func.sum(PartCosts.volume).label('total_volume'),
        Idea.target_cost, 
        Idea.confirmed_cost, 
        Idea.toggle_active, 

    ).join(PartHasIdea, Part.id == PartHasIdea.part_id).join(Idea, PartHasIdea.idea_id == Idea.id).join(Idea.volumes, isouter=True).group_by(
        Part.id,
        Part.part_number,
        Part.description,
        Idea.id,
        Idea.source,
        Idea.type,
        Idea.description,
        Idea.alternate_pn,
        Idea.status,
        Idea.il,
        Idea.notes,
        Idea.baseline_cost_source,
        PartCosts.cost,
        Idea.target_cost,
        Idea.confirmed_cost,
        Idea.toggle_active,
    )

    results = query.all()
    session.close()
    
    return results

def get_parts():
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
        Part.id,
        Part.part_number, 
        Part.description,         
    ).limit(1000)
    results = query.all()
    session.close()
    return results

def get_part_numbers():
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
        Part.part_number,         
    ).limit(1000)
    results = query.all()
    session.close()
    return results

def get_searched_parts(search_string):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Building the query with an OR condition for search_string in any column
    query = session.query(
        Part.id,
        Part.part_number, 
        Part.description,         
        
    ).filter(
        or_(
            Part.part_number.like(f"%{search_string}%"), 
            Part.description.like(f"%{search_string}%"), 
        )
    )
    
    results = query.all()
    session.close()
    return results

def get_searched_part_numbers(search_string):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Building the query with an OR condition for search_string in any column
    query = session.query(
        Part.part_number,         
        
    ).filter(
        or_(
            Part.part_number.like(f"%{search_string}%"), 
        )
    )
    
    results = query.all()
    session.close()
    return results

def get_component_library_part_number(part_name):
    # engine = create_engine(dbstring)
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # # Perform a join between Spendcube and Part on spendcube.part == part.part_number
    # # Assuming there's a PartCosts model with a relationship to Part named 'prices'
    # # and it has a 'price' attribute. Replace 'PartCosts.price' with the actual way to access price.
    # query = session.query(
    #     Spendcube.part,
    #     Spendcube.mpn,
    #     Part.description,
    #     Spendcube.supplier_name_standardized,
    #     Spendcube.price,
    #     Spendcube.quantity
    # ).join(
    #     Part, Spendcube.part == Part.part_number
    # )

    # results = query.all()
    # session.close()
    # return results
    engine = create_engine(dbstring, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Assuming the Part model is linked to the Spendcube model via a foreign key.
    # Also assuming that there is a PartCosts model linked to Part with a foreign key,
    # and it contains a 'cost' field and a 'volume' field.
    query = session.query(
        Spendcube.part,
        Spendcube.mpn,
        Part.description,
        Spendcube.supplier_name_standardized,
        func.Spendcube.price.label('recent_price'),
        func.sum(Spendcube.quantity).label('total_quantity'),
        func.max(Spendcube.invoice_date).label('recent_invoice_date')
    ).join(
        Part, Spendcube.part == Part.part_number
    ).filter(
        Spendcube.part == part_name
    ).group_by(
        Spendcube.part,
        Spendcube.mpn,
        Part.description,
        Spendcube.supplier_name_standardized,
    )

    results = query.all()
    session.close()

    return results


def update_ideas(ideas):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for idea in ideas:
        try:
            id = idea['Idea ID']
            update_values = { 
                'source' : idea['Source'], 
                'type' : idea['Type'], 
                'description' : idea['Description'], 
                # 'scope' : idea['Idea Scope'],
                'alternate_pn' : idea['Alternate MPN'], 
                'target_cost' : idea['Target Cost'], 
                'confirmed_cost' : idea['Confirmed New Cost'], 
                'toggle_active' : idea['Count in Savings'], 
                'notes' : idea['Notes'], 
                'il' : idea['IL Status'], 
                'status' : idea['Status'], 
            }
            print("Update Values: ",update_values)
            # Fetch the IDEA record to update
            record = session.query(Idea).filter(Idea.id == id).first()
            if not record:
                print(f"No IDEA record found with ID {id}.")
                return
            
            # Update IDEA attributes
            attrs = ['source', 
            'type', 
            'description', 
            # 'scope',
            'alternate_pn', 
            'target_cost', 
            'confirmed_cost', 
            'toggle_active',
            'notes',
            'il',
            'status']
            for attr in attrs:
                if attr in update_values:
                    setattr(record, attr, update_values[attr])
            # Commit the changes
            session.commit()
            print(f"IDEA record with ID {id} has been updated.")
        except SQLAlchemyError as e:
            session.rollback()  # Rollback the changes in case of error
            print(f"An error occurred: {e}")
        finally:
            session.close()  # Close the session

def add_idea_with_parts(
    partIDs,
    source,
    type, 
    description,
    alternate_pn, 
    target_cost,
    new_il,
    new_status,
    new_notes):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Create a new Idea object
        new_idea = Idea(
            source=source,
            type=type,
            description=description,
            alternate_pn=alternate_pn,
            target_cost=target_cost,
            il=new_il,
            status=new_status,
            notes=new_notes
        )
        session.add(new_idea)
        session.flush()  # This ensures new_idea gets its ID before we use it below

        # Associate parts with the new idea
        for partID in partIDs:
            association = PartHasIdea(
                part_id=partID,
                idea_id=new_idea.id
            )
            print(id, association)
            session.add(association)
        session.commit()  # Commit all changes after all records are added
        # print("Idea and associations have been added successfully.")
    except Exception as e:
        session.rollback()  # Rollback the changes on error
        print(f"An error occurred: {e}")
    else:
        print("Idea added successfully")
        session.close()  # Close the session to free resources

def delete_ideas(ids):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print(ids)
    try:
        query = session.query(Idea).filter(Idea.id.in_(ids))
        deleted_count = query.delete(synchronize_session=False)  # You can use 'fetch' or 'evaluate' as well
        session.commit()
        print(f"Deleted {deleted_count} rows.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occured: {e}")  
    finally:
        session.close()


# TODO CHECK THIS FUNCTION
def add_bom(product_info):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Extract product details
    product_number = product_info['product_number']
    product_description = product_info['product_description']
    
    # Check if product exists
    product = session.query(Product).filter_by(product_number=product_number).first()
    if not product:
        # Insert new product if not exists
        product = Product(product_number=product_number, product_description=product_description)
        session.add(product)
        session.commit()

    # Iterate over parts in the product_info
    for part in product_info['parts']:
        part_number = part['part_number']
        part_description = part['part_description']
        
        # Check if part exists
        part_record = session.query(Part).filter_by(part_number=part_number).first()
        if not part_record:
            # Insert new part if not exists
            part_record = Part(part_number=part_number, part_description=part_description)
            session.add(part_record)
            session.commit()
        
        # Prepare PartInProduct
        pip = PartInProduct(
            part_id=part_record.id,
            product_id=product.id,
            bom_description=part.get('bom_description', ''),
            bom_cost=part.get('bom_cost', 0),
            bom_quantity=part.get('bom_quantity', 0),
            bom_supplier=part.get('bom_supplier', ''),
            export_rating=part.get('export_rating', '')
        )
        
        # Check if the PartInProduct exists
        existing_pip = session.query(PartInProduct).filter_by(part_id=pip.part_id, product_id=pip.product_id).first()
        if not existing_pip:
            session.add(pip)
        
    session.commit()
    
def get_part_costs(part_id):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(
        PartCosts.type,
        PartCosts.source,
        PartCosts.cost,
        PartCosts.volume,
        PartCosts.datetime_added,
        ).filter(PartCosts.part_id == part_id)
    results = query.all()
    session.close()
    return results


def add_costs(part_id, costs):
    engine = create_engine(dbstring)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for cost in costs:
        print(cost)
        try:
            new_cost = PartCosts(
                part_id = part_id,
                cost = cost['Cost'],
                volume = cost['Volume'],
                source = cost['Source'],
                type = cost['Type'],
                datetime_added = cost['Date Added'])
            session.add(new_cost)
            session.commit()
        except Exception as e:
            session.rollback()  # Rollback the changes on error
            print(f"An error occurred: {e}")
        else:
            print("Cost added")
            session.close()